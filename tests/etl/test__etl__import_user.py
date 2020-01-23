import pytest
from unittest.mock import patch
from portal.etl.database import user_table, etl_practice_database
from portal.etl import import_user
from portal.models import User
from portal.database import db
from tests.etl.test__etl__import_practice import _create_db_practices

@pytest.mark.parametrize(
    "user_count",
    [0, 1, 2, 3],
)
def test__ok__imports_users(client, etl_practice_db, faker, user_count):

    users = [faker.etl_user_details() for _ in range(user_count)]
    _create_etl_users(etl_practice_db, users)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_user()

    _assert_users_exist(users)


def test__existing__update(client, etl_practice_db, faker):

    users = [faker.etl_user_details() for id in range(3)]
    _create_db_users(users)

    new_name = faker.company()

    users[2]['name'] = new_name

    _create_etl_users(etl_practice_db, users)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_user()

    _assert_users_exist(users)


@pytest.mark.parametrize(
    "removed_count",
    [0, 1, 2, 3],
)
def test__removed__delete(client, etl_practice_db, faker, removed_count):

    users = [faker.etl_user_details() for id in range(3)]
    users_to_be_added = [faker.etl_user_details() for _ in range(2)]
    users_to_be_removed = [faker.etl_user_details() for id in range(removed_count)]
    _create_db_users(users + users_to_be_removed)

    _create_etl_users(etl_practice_db, users + users_to_be_added)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_user()

    _assert_users_exist(users)
    _assert_users_do_not_exist(users_to_be_removed)


def test__ok__imports_links_to_practices(client, etl_practice_db, faker):

    practice_a = faker.etl_practice_details()
    practice_a['practice_code'] = 'C12345'

    practice_b = faker.etl_practice_details()
    practice_b['practice_code'] = 'C54321'

    practices = [practice_a, practice_b]
    _create_db_practices(practices)

    u_pa = faker.etl_user_details()
    u_pa['practice_code'] = practice_a['practice_code']

    u_pb = u_pa.copy()
    u_pb['practice_code'] = practice_b['practice_code']

    users = [u_pa, u_pb]

    _create_etl_users(etl_practice_db, users)

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_user()

    _assert_users_exist(users)
    _assert_user_practices(u_pa['email'], practices)


def _create_etl_users(etl_practice_db, users):
    for p in users:
        etl_practice_db.execute(
            user_table.insert(),
            project_id=p['project_id'],
            practice_code=p['practice_code'],
            email=p['email'],
            current_portal_user_yn=p['current_portal_user_yn'],
            gv_end_del_log=p['gv_end_del_log'],
        )


def _create_db_users(users):
    db.session.add_all(
        [User(
            project_id=p['project_id'],
            email=p['email'],
            current_portal_user_yn=p['current_portal_user_yn'],
            gv_end_del_log=p['gv_end_del_log'],
        ) for p in users]
    )
    db.session.commit()


def _assert_users_exist(expected):
    for e in expected:
        actual = User.query.filter_by(email=e['email']).one_or_none()

        assert actual is not None

        assert actual.project_id == e['project_id']
        assert actual.email == e['email']
        assert actual.current_portal_user_yn == e['current_portal_user_yn']
        assert actual.gv_end_del_log == e['gv_end_del_log']


def _assert_users_do_not_exist(not_expected):
    for ne in not_expected:
        actual = User.query.filter_by(email=ne['email']).one_or_none()

        assert actual is None


def _assert_user_practices(email, practices):
    actual = User.query.filter_by(email=email).one_or_none()

    assert actual is not None

    assert [p['practice_code'] for p in practices] == [p.code for p in actual.practices]
