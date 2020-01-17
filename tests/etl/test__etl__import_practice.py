import pytest
from unittest.mock import patch
from portal.etl.database import practice_table, etl_practice_database
from portal.etl import import_practice
from portal.models import Practice

@pytest.mark.parametrize(
    "practice_count",
    [0, 1, 2, 3],
)
def test__ok__imports_practices(client, etl_practice_db, faker, practice_count):

    practices = [faker.etl_practice_details() for _ in range(practice_count)]
    _create_test_practices(etl_practice_db, practices)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_practice()

    _assert_practices_exist(practices)


def _create_test_practices(etl_practice_db, practices):
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


def _assert_practices_exist(expected):
    for e in expected:
        actual = Practice.query.filter_by(code=e['practice_code']).one_or_none()

        assert actual is not None
        assert actual.code == e['practice_code']
        assert actual.name == e['practice_name']
        assert actual.ccg_id == e['ccg']
        assert actual.address == e['practice_address']
        assert actual.partners == e['partners']