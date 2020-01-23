import pytest
from unittest.mock import patch
from portal.etl.database import management_area_table, etl_practice_database
from portal.etl import import_areas
from portal.models import ManagementArea
from portal.database import db

@pytest.mark.parametrize(
    "area_count",
    [0, 1, 2, 3],
)
def test__new__import(client, etl_practice_db, faker, area_count):

    areas = [faker.etl_area_details(id) for id in range(area_count)]
    _create_etl_areas(etl_practice_db, areas)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_areas()

    _assert_areas_exist(areas)


def test__existing__update(client, etl_practice_db, faker):

    areas = [faker.etl_area_details(id) for id in range(3)]
    _create_db_areas(areas)

    new_name = faker.company()

    areas[2]['name'] = new_name

    _create_etl_areas(etl_practice_db, areas)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_areas()

    _assert_areas_exist(areas)


@pytest.mark.parametrize(
    "removed_count",
    [0, 1, 2, 3],
)
def test__removed__delete(client, etl_practice_db, faker, removed_count):

    areas = [faker.etl_area_details(id) for id in range(3)]
    areas_to_be_added = [faker.etl_area_details(id) for id in range(4, 6)]
    areas_to_be_removed = [faker.etl_area_details(id) for id in range(6, removed_count + 6)]
    _create_db_areas(areas + areas_to_be_removed)

    _create_etl_areas(etl_practice_db, areas + areas_to_be_added)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_areas()

    _assert_areas_exist(areas)
    _assert_areas_does_not_exist(areas_to_be_removed)


def _create_etl_areas(etl_practice_db, areas):
    for c in areas:
        etl_practice_db.execute(
            management_area_table.insert(),
            project_id=c['project_id'],
            name=c['name'],
        )


def _create_db_areas(areas):
    db.session.add_all(
        [ManagementArea(
            project_id=a['project_id'],
            name=a['name'],
        ) for a in areas]
    )
    db.session.commit()


def _assert_areas_exist(expected):
    for e in expected:
        actual = ManagementArea.query.filter_by(
            project_id=e['project_id'],
        ).one_or_none()

        assert actual is not None
        assert actual.project_id == e['project_id']
        assert actual.identifier is None
        assert actual.name == e['name']


def _assert_areas_does_not_exist(not_expected):
    for ne in not_expected:
        actual = ManagementArea.query.filter_by(
            project_id=ne['project_id'],
        ).one_or_none()

        assert actual is None
