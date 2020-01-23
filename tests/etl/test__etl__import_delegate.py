import pytest
from unittest.mock import patch
from portal.etl.database import delegate_table, etl_practice_database
from portal.etl import import_delegate
from portal.models import Delegate
from portal.database import db

@pytest.mark.parametrize(
    "delegate_count",
    [0, 1, 2, 3],
)
def test__ok__imports_delegates(client, etl_practice_db, faker, delegate_count):

    delegates = [faker.etl_delegate_details() for _ in range(delegate_count)]
    _create_etl_delegates(etl_practice_db, delegates)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_delegate()

    _assert_delegates_exist(delegates)


def test__existing__update(client, etl_practice_db, faker):

    delegates = [faker.etl_delegate_details() for id in range(3)]
    _create_db_delegates(delegates)

    new_name = faker.company()

    delegates[2]['name'] = new_name

    _create_etl_delegates(etl_practice_db, delegates)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_delegate()

    _assert_delegates_exist(delegates)


@pytest.mark.parametrize(
    "removed_count",
    [0, 1, 2, 3],
)
def test__removed__delete(client, etl_practice_db, faker, removed_count):

    delegates = [faker.etl_delegate_details() for id in range(3)]
    delegates_to_be_added = [faker.etl_delegate_details() for _ in range(2)]
    delegates_to_be_removed = [faker.etl_delegate_details() for id in range(removed_count)]
    _create_db_delegates(delegates + delegates_to_be_removed)

    _create_etl_delegates(etl_practice_db, delegates + delegates_to_be_added)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_delegate()

    _assert_delegates_exist(delegates)
    _assert_delegates_do_not_exist(delegates_to_be_removed)


def _create_etl_delegates(etl_practice_db, delegates):
    for p in delegates:
        etl_practice_db.execute(
            delegate_table.insert(),
            project_id=p['project_id'],
            practice_code=p['practice_code'],
            instance=p['instance'],
            name=p['name'],
            role=p['role'],
            gcp_trained=p['gcp_trained'],
            gv_trained=p['gv_trained'],
            on_delegation_log_yn=p['on_delegation_log_yn'],
            gv_start_del_log=p['gv_start_del_log'],
            gv_end_del_log=p['gv_end_del_log'],
            gv_phone_a=p['gv_phone_a'],
            gv_phone_b=p['gv_phone_b'],
            contact_email_add=p['contact_email_add'],
            primary_contact_yn=p['primary_contact_yn'],
        )


def _create_db_delegates(delegates):
    db.session.add_all(
        [Delegate(
            project_id=p['project_id'],
            practice_code=p['practice_code'],
            instance=p['instance'],
            name=p['name'],
            role=p['role'],
            gcp_trained=p['gcp_trained'],
            gv_trained=p['gv_trained'],
            on_delegation_log_yn=p['on_delegation_log_yn'],
            gv_start_del_log=p['gv_start_del_log'],
            gv_end_del_log=p['gv_end_del_log'],
            gv_phone_a=p['gv_phone_a'],
            gv_phone_b=p['gv_phone_b'],
            contact_email_add=p['contact_email_add'],
            primary_contact_yn=p['primary_contact_yn'],
        ) for p in delegates]
    )
    db.session.commit()


def _assert_delegates_exist(expected):
    for e in expected:
        actual = Delegate.query.filter_by(
            project_id=e['project_id'],
            practice_code=e['practice_code'],
            instance=e['instance'],
        ).one_or_none()

        assert actual is not None

        assert actual.project_id == e['project_id']
        assert actual.practice_code == e['practice_code']
        assert actual.instance == e['instance']
        assert actual.name == e['name']
        assert actual.role == e['role']
        assert actual.gcp_trained == e['gcp_trained']
        assert actual.gv_trained == e['gv_trained']
        assert actual.on_delegation_log_yn == e['on_delegation_log_yn']
        assert actual.gv_start_del_log == e['gv_start_del_log']
        assert actual.gv_end_del_log == e['gv_end_del_log']
        assert actual.gv_phone_a == e['gv_phone_a']
        assert actual.gv_phone_b == e['gv_phone_b']
        assert actual.contact_email_add == e['contact_email_add']
        assert actual.primary_contact_yn == e['primary_contact_yn']

def _assert_delegates_do_not_exist(not_expected):
    for ne in not_expected:
        actual = Delegate.query.filter_by(
            project_id=ne['project_id'],
            practice_code=ne['practice_code'],
            instance=ne['instance'],
        ).one_or_none()

        assert actual is None
