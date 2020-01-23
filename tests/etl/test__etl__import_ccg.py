import pytest
from unittest.mock import patch
from portal.etl.database import ccg_table, etl_practice_database
from portal.etl import import_ccg
from portal.models import Ccg
from portal.database import db

@pytest.mark.parametrize(
    "ccg_count",
    [0, 1, 2, 3],
)
def test__new__import(client, etl_practice_db, faker, ccg_count):

    ccgs = [faker.etl_ccg_details(id) for id in range(ccg_count)]
    _create_etl_ccgs(etl_practice_db, ccgs)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_ccg()

    _assert_ccgs_exist(ccgs)


def test__existing__update(client, etl_practice_db, faker):

    ccgs = [faker.etl_ccg_details(id) for id in range(3)]
    _create_db_ccgs(ccgs)

    new_name = faker.company()

    ccgs[2]['name'] = new_name

    _create_etl_ccgs(etl_practice_db, ccgs)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_ccg()

    _assert_ccgs_exist(ccgs)


@pytest.mark.parametrize(
    "removed_count",
    [0, 1, 2, 3],
)
def test__removed__delete(client, etl_practice_db, faker, removed_count):

    ccgs = [faker.etl_ccg_details(id) for id in range(3)]
    ccgs_to_be_added = [faker.etl_ccg_details(id) for id in range(4, 6)]
    ccgs_to_be_removed = [faker.etl_ccg_details(id) for id in range(6, removed_count + 6)]
    _create_db_ccgs(ccgs + ccgs_to_be_removed)

    _create_etl_ccgs(etl_practice_db, ccgs + ccgs_to_be_added)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_ccg()

    _assert_ccgs_exist(ccgs)
    _assert_ccgs_does_not_exist(ccgs_to_be_removed)


def _create_etl_ccgs(etl_practice_db, ccgs):
    for c in ccgs:        
        etl_practice_db.execute(
            ccg_table.insert(),
            project_id=c['project_id'],
            ccg_id=c['ccg_id'],
            name=c['name'],
        )


def _create_db_ccgs(ccgs):
    print(ccgs)
    db.session.add_all(
        [Ccg(
            project_id=c['project_id'],
            identifier=c['ccg_id'],
            name=c['name'],
        ) for c in ccgs]
    )
    db.session.commit()


def _assert_ccgs_exist(expected):
    for e in expected:
        actual = Ccg.query.filter_by(
            project_id=e['project_id'],
            identifier=e['ccg_id'],
        ).one_or_none()

        assert actual is not None
        assert actual.project_id == e['project_id']
        assert actual.identifier == e['ccg_id']
        assert actual.name == e['name']


def _assert_ccgs_does_not_exist(not_expected):
    for ne in not_expected:
        actual = Ccg.query.filter_by(
            project_id=ne['project_id'],
            identifier=ne['ccg_id'],
        ).one_or_none()

        assert actual is None
