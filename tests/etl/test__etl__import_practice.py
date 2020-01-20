import pytest
from unittest.mock import patch
from portal.etl.database import practice_table, etl_practice_database
from portal.etl import import_practice
from portal.models import Practice
from portal.database import db

@pytest.mark.parametrize(
    "practice_count",
    [0, 1, 2, 3],
)
def test__ok__imports_practices(client, etl_practice_db, faker, practice_count):

    practices = [faker.etl_practice_details() for _ in range(practice_count)]
    _create_etl_practices(etl_practice_db, practices)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_practice()

    _assert_practices_exist(practices)


def test__existing__update(client, etl_practice_db, faker):

    practices = [faker.etl_practice_details() for id in range(3)]
    _create_db_practices(practices)

    new_name = faker.company()

    practices[2]['name'] = new_name

    _create_etl_practices(etl_practice_db, practices)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_practice()

    _assert_practices_exist(practices)


@pytest.mark.parametrize(
    "removed_count",
    [0, 1, 2, 3],
)
def test__removed__delete(client, etl_practice_db, faker, removed_count):

    practices = [faker.etl_practice_details() for id in range(3)]
    practices_to_be_added = [faker.etl_practice_details() for _ in range(2)]
    practices_to_be_removed = [faker.etl_practice_details() for id in range(removed_count)]
    _create_db_practices(practices + practices_to_be_removed)

    _create_etl_practices(etl_practice_db, practices + practices_to_be_added)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_practice()

    _assert_practices_exist(practices)
    _assert_practices_do_not_exist(practices_to_be_removed)


def _create_etl_practices(etl_practice_db, practices):
    for p in practices:
        etl_practice_db.execute(
            practice_table.insert(),
            project_id=p['project_id'],
            practice_code=p['practice_code'],
            practice_name=p['practice_name'],
            ccg=p['ccg'],
            practice_address=p['practice_address'],
            pract_town=p['pract_town'],
            city=p['city'],
            county=p['county'],
            postcode=p['postcode'],
            federation=p['federation'],
            partners=p['partners'],
            genvasc_initiated=p['genvasc_initiated'],
            status=p['status'],
        )


def _create_db_practices(practices):
    db.session.add_all(
        [Practice(
            project_id=p['project_id'],
            code=p['practice_code'],
            name=p['practice_name'],
            ccg_id=p['ccg'],
            street_address=p['practice_address'],
            town=p['pract_town'],
            city=p['city'],
            county=p['county'],
            postcode=p['postcode'],
            federation=p['federation'],
            partners=p['partners'],
            genvasc_initiated=p['genvasc_initiated'],
            status=p['status'],
        ) for p in practices]
    )
    db.session.commit()


def _assert_practices_exist(expected):
    for e in expected:
        actual = Practice.query.filter_by(code=e['practice_code']).one_or_none()

        assert actual is not None

        assert actual.project_id == e['project_id']
        assert actual.code == e['practice_code']
        assert actual.name == e['practice_name']
        assert actual.ccg_id == e['ccg']
        assert actual.street_address == e['practice_address']
        assert actual.town == e['pract_town']
        assert actual.city == e['city']
        assert actual.county == e['county']
        assert actual.postcode == e['postcode']
        assert actual.federation == e['federation']
        assert actual.partners == e['partners']
        assert actual.genvasc_initiated == e['genvasc_initiated']
        assert actual.status == e['status']

def _assert_practices_do_not_exist(not_expected):
    for ne in not_expected:
        actual = Practice.query.filter_by(
            code=ne['practice_code'],
        ).one_or_none()

        assert actual is None
