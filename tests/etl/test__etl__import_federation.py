import pytest
from unittest.mock import patch
from portal.etl.database import federation_table, etl_practice_database
from portal.etl import import_federation
from portal.models import Federation
from portal.database import db

@pytest.mark.parametrize(
    "federation_count",
    [0, 1, 2, 3],
)
def test__new__import(client, etl_practice_db, faker, federation_count):

    federations = [faker.etl_federation_details(id) for id in range(federation_count)]
    _create_etl_federations(etl_practice_db, federations)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_federation()

    _assert_federations_exist(federations)


def test__existing__update(client, etl_practice_db, faker):

    federations = [faker.etl_federation_details(id) for id in range(3)]
    _create_db_federations(federations)

    new_name = faker.company()

    federations[2]['name'] = new_name

    _create_etl_federations(etl_practice_db, federations)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_federation()

    _assert_federations_exist(federations)


@pytest.mark.parametrize(
    "removed_count",
    [0, 1, 2, 3],
)
def test__removed__delete(client, etl_practice_db, faker, removed_count):

    federations = [faker.etl_federation_details(id) for id in range(3)]
    federations_to_be_added = [faker.etl_federation_details(id) for id in range(4, 6)]
    federations_to_be_removed = [faker.etl_federation_details(id) for id in range(6, removed_count + 6)]
    _create_db_federations(federations + federations_to_be_removed)

    _create_etl_federations(etl_practice_db, federations + federations_to_be_added)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_federation()

    _assert_federations_exist(federations)
    _assert_federations_does_not_exist(federations_to_be_removed)


def _create_etl_federations(etl_practice_db, federations):
    for c in federations:        
        etl_practice_db.execute(
            federation_table.insert(),
            project_id=c['project_id'],
            federation_id=c['federation_id'],
            name=c['name'],
        )


def _create_db_federations(federations):
    db.session.add_all(
        [Federation(
            project_id=c['project_id'],
            identifier=c['federation_id'],
            name=c['name'],
        ) for c in federations]
    )
    db.session.commit()


def _assert_federations_exist(expected):
    for e in expected:
        actual = Federation.query.filter_by(
            project_id=e['project_id'],
            identifier=e['federation_id'],
        ).one_or_none()

        assert actual is not None
        assert actual.project_id == e['project_id']
        assert actual.identifier == e['federation_id']
        assert actual.name == e['name']


def _assert_federations_does_not_exist(not_expected):
    for ne in not_expected:
        actual = Federation.query.filter_by(
            project_id=ne['project_id'],
            identifier=ne['federation_id'],
        ).one_or_none()

        assert actual is None
