import pytest
from unittest.mock import patch
from portal.etl.database import ccg_table, etl_practice_database
from portal.etl import import_ccg
from portal.models import Ccg

@pytest.mark.parametrize(
    "ccg_count",
    [0, 1, 2, 3],
)
def test__ok__imports_ccgs(client, etl_practice_db, faker, ccg_count):

    ccgs = [faker.etl_ccg_details(id) for id in range(1, ccg_count)]
    _create_test_ccgs(etl_practice_db, ccgs)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_ccg()

    _assert_ccgs_exist(ccgs)


def _create_test_ccgs(etl_practice_db, ccgs):
    for c in ccgs:        
        etl_practice_db.execute(
            ccg_table.insert(),
            project_id=c['project_id'],
            ccg_id=c['ccg_id'],
            name=c['name'],
        )


def _assert_ccgs_exist(expected):
    for e in expected:
        actual = Ccg.query.filter_by(
            project_id=e['project_id'],
            id=e['ccg_id'],
        ).one_or_none()

        assert actual is not None
        assert actual.project_id == e['project_id']
        assert actual.id == e['ccg_id']
        assert actual.name == e['name']
