import pytest
from unittest.mock import patch
from portal.etl.database import practice_table, etl_practice_database
from portal.etl import import_practice
from portal.models import (
    Practice,
    PracticeRegistration,
    Ccg,
    Federation,
    ManagementArea,
)
from portal.database import db
from tests.etl.test__etl__import_ccg import _create_db_ccgs
from tests.etl.test__etl__import_federation import _create_db_federations
from tests.etl.test__etl__import_management_area import _create_db_areas


@pytest.mark.parametrize(
    "practice_count",
    [0, 1, 2, 3],
)
def test__ok__imports_practices(client, etl_practice_db, faker, practice_count):

    practices = [faker.etl_practice_details() for _ in range(practice_count)]
    _create_etl_practices(etl_practice_db, practices)

    _create_db_ccgs([faker.etl_ccg_details(1)])
    _create_db_federations([faker.etl_federation_details(1)])
    _create_db_areas([faker.etl_area_details(1)])

    with patch('portal.etl.etl_practice_database') as mock_etl_practice_database:
        mock_etl_practice_database.return_value.__enter__.return_value = etl_practice_db

        import_practice()

    _assert_practices_exist(practices)


def test__existing__update(client, etl_practice_db, faker):

    practices = [faker.etl_practice_details() for id in range(3)]
    _create_db_practices(practices)

    _create_db_ccgs([faker.etl_ccg_details(1)])
    _create_db_federations([faker.etl_federation_details(1)])
    _create_db_areas([faker.etl_area_details(1)])

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

    _create_db_ccgs([faker.etl_ccg_details(1)])
    _create_db_federations([faker.etl_federation_details(1)])
    _create_db_areas([faker.etl_area_details(1)])

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
            code=p['practice_code'],
            name=p['practice_name'],
            street_address=p['practice_address'],
            town=p['pract_town'],
            city=p['city'],
            county=p['county'],
            postcode=p['postcode'],
            partners=p['partners'],
            genvasc_initiated=p['genvasc_initiated'],
            status=p['status'],
        ) for p in practices]
    )
    db.session.add_all(
        [PracticeRegistration(
            code=p['practice_code'],
        ) for p in practices]
    )
    db.session.commit()


def _assert_practices_exist(expected):
    for e in expected:
        actual = Practice.query.filter_by(code=e['practice_code']).one_or_none()

        assert actual is not None

        assert actual.code == e['practice_code']
        assert actual.name == e['practice_name']
        assert actual.street_address == e['practice_address']
        assert actual.town == e['pract_town']
        assert actual.city == e['city']
        assert actual.county == e['county']
        assert actual.postcode == e['postcode']
        assert actual.partners == e['partners']
        assert actual.genvasc_initiated == e['genvasc_initiated']
        assert actual.status == e['status']
        assert any(
            g for g in actual.groups
            if g.identifier == e['ccg'] and isinstance(g, Ccg)
        )
        assert any(
            g for g in actual.groups
            if g.identifier == e['federation'] and isinstance(g, Federation)
        )
        assert any(
            g for g in actual.groups
            if g.project_id == e['project_id'] and isinstance(g, ManagementArea)
        )

        assert PracticeRegistration.query.filter_by(
            code=e['practice_code'],
        ).one_or_none() is not None


def _assert_practices_do_not_exist(not_expected):
    for ne in not_expected:
        assert Practice.query.filter_by(
            code=ne['practice_code'],
        ).one_or_none() is None

        assert PracticeRegistration.query.filter_by(
            code=ne['practice_code'],
        ).one_or_none() is None
