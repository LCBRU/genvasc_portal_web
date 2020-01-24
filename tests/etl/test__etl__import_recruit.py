import pytest
from unittest.mock import patch
from portal.etl.database import recruit_table, etl_recruit_database
from portal.etl import import_recruit
from portal.models import Recruit, Practice
from portal.database import db
from tests.etl.test__etl__import_practice import _create_db_practices
from pprint import pprint as pp

@pytest.mark.parametrize(
    "recruit_count",
    [0, 1, 2, 3],
)
def test__new__import_not_processed(client, etl_recruit_db, faker, recruit_count):

    practice = faker.etl_practice_details()
    _create_db_practices([practice])

    recruits = [faker.etl_recruit_details_not_processed(practice_code=practice['practice_code']) for id in range(recruit_count)]
    _create_etl_recruits(etl_recruit_db, recruits)

    with patch('portal.etl.etl_recruit_database') as mock_etl_recruit_database:
        mock_etl_recruit_database.return_value.__enter__.return_value = etl_recruit_db

        import_recruit()

    _assert_recruits_exist(recruits)


def test__existing__update_not_processed(client, etl_recruit_db, faker):

    practice = faker.etl_practice_details()
    _create_db_practices([practice])

    recruits = [faker.etl_recruit_details_not_processed(practice_code=practice['practice_code']) for id in range(3)]
    _create_db_recruits(recruits)

    new_name = faker.company()

    recruits[2]['name'] = new_name

    _create_etl_recruits(etl_recruit_db, recruits)

    with patch('portal.etl.etl_recruit_database') as mock_etl_recruit_database:
        mock_etl_recruit_database.return_value.__enter__.return_value = etl_recruit_db

        import_recruit()

    _assert_recruits_exist(recruits)


@pytest.mark.parametrize(
    "recruit_count",
    [0, 1, 2, 3],
)
def test__new__import_processed(client, etl_recruit_db, faker, recruit_count):

    practice = faker.etl_practice_details()
    _create_db_practices([practice])

    recruits = [faker.etl_recruit_details_processed(practice_code=practice['practice_code']) for id in range(recruit_count)]
    _create_etl_recruits(etl_recruit_db, recruits)

    with patch('portal.etl.etl_recruit_database') as mock_etl_recruit_database:
        mock_etl_recruit_database.return_value.__enter__.return_value = etl_recruit_db

        import_recruit()

    _assert_recruits_exist(recruits)


def test__existing__update_processed(client, etl_recruit_db, faker):

    practice = faker.etl_practice_details()
    _create_db_practices([practice])

    recruits = [faker.etl_recruit_details_processed(practice_code=practice['practice_code']) for id in range(3)]
    _create_db_recruits(recruits)

    new_name = faker.company()

    recruits[2]['name'] = new_name

    _create_etl_recruits(etl_recruit_db, recruits)

    with patch('portal.etl.etl_recruit_database') as mock_etl_recruit_database:
        mock_etl_recruit_database.return_value.__enter__.return_value = etl_recruit_db

        import_recruit()

    _assert_recruits_exist(recruits)


@pytest.mark.parametrize(
    "removed_count",
    [0, 1, 2, 3],
)
def test__removed__delete__not_processed(client, etl_recruit_db, faker, removed_count):

    practice = faker.etl_practice_details()
    _create_db_practices([practice])

    recruits = [faker.etl_recruit_details_not_processed(practice_code=practice['practice_code']) for id in range(3)]
    recruits_to_be_added = [faker.etl_recruit_details_not_processed(practice_code=practice['practice_code']) for id in range(4, 6)]
    recruits_to_be_removed = [faker.etl_recruit_details_not_processed(practice_code=practice['practice_code']) for id in range(6, removed_count + 6)]
    _create_db_recruits(recruits + recruits_to_be_removed)

    _create_etl_recruits(etl_recruit_db, recruits + recruits_to_be_added)

    with patch('portal.etl.etl_recruit_database') as mock_etl_recruit_database:
        mock_etl_recruit_database.return_value.__enter__.return_value = etl_recruit_db

        import_recruit()

    _assert_recruits_exist(recruits)
    _assert_recruits_does_not_exist(recruits_to_be_removed)


@pytest.mark.parametrize(
    "removed_count",
    [0, 1, 2, 3],
)
def test__removed__delete__processed(client, etl_recruit_db, faker, removed_count):

    practice = faker.etl_practice_details()
    _create_db_practices([practice])

    recruits = [faker.etl_recruit_details_processed(practice_code=practice['practice_code']) for id in range(3)]
    recruits_to_be_added = [faker.etl_recruit_details_processed(practice_code=practice['practice_code']) for id in range(4, 6)]
    recruits_to_be_removed = [faker.etl_recruit_details_processed(practice_code=practice['practice_code']) for id in range(6, removed_count + 6)]
    _create_db_recruits(recruits + recruits_to_be_removed)

    _create_etl_recruits(etl_recruit_db, recruits + recruits_to_be_added)

    with patch('portal.etl.etl_recruit_database') as mock_etl_recruit_database:
        mock_etl_recruit_database.return_value.__enter__.return_value = etl_recruit_db

        import_recruit()

    _assert_recruits_exist(recruits)
    _assert_recruits_does_not_exist(recruits_to_be_removed)


def _create_etl_recruits(etl_recruit_db, recruits):
    for c in recruits:
        etl_recruit_db.execute(
            recruit_table.insert(),
            processing_id=c['processing_id'],
            status=c['status'],
            nhs_number=c['nhs_number'],
            study_id=c['study_id'],
            practice_code=c['practice_code'],
            first_name=c['first_name'],
            last_name=c['last_name'],
            date_of_birth=c['date_of_birth'],
            civicrm_contact_id=c['civicrm_contact_id'],
            civicrm_case_id=c['civicrm_case_id'],
            processed_date=c['processed_date'],
            recruited_date=c['recruited_date'],
            invoice_year=c['invoice_year'],
            invoice_quarter=c['invoice_quarter'],
            reimbursed_status=c['reimbursed_status'],
        )


def _create_db_recruits(recruits):
    for r in recruits:
        p = Practice.query.filter_by(code=r['practice_code']).one_or_none()

        db.session.add(
            Recruit(
                practice_id=p.id,
                processing_id=r['processing_id'],
                nhs_number=r['nhs_number'],
                date_of_birth=r['date_of_birth'],
                date_recruited=r['recruited_date'],
                status=r['status'],
                study_id=r['study_id'],
                first_name=r['first_name'],
                last_name=r['last_name'],
                processed_date=r['processed_date'],
                invoice_year=r['invoice_year'],
                invoice_quarter=r['invoice_quarter'],
                reimbursed_status=r['reimbursed_status'],
            )
        )

    db.session.commit()


def _assert_recruits_exist(expected):
    for e in expected:
        p = Practice.query.filter_by(code=e['practice_code']).one_or_none()

        if e['processing_id'] is not None:
            actual = Recruit.query.filter_by(
                processing_id=e['processing_id'],
            ).one_or_none()
        else:
            actual = Recruit.query.filter_by(
                civicrm_case_id=e['civicrm_case_id'],
            ).one_or_none()

        assert actual is not None
        assert actual.practice_id == p.id
        assert actual.processing_id == e['processing_id']
        assert actual.nhs_number == e['nhs_number']
        assert actual.date_of_birth == e['date_of_birth']
        assert actual.date_recruited == e['recruited_date']
        assert actual.status == e['status']
        assert actual.study_id == e['study_id']
        assert actual.first_name == e['first_name']
        assert actual.last_name == e['last_name']
        assert actual.processed_date == e['processed_date']
        assert actual.invoice_year == e['invoice_year']
        assert actual.invoice_quarter == e['invoice_quarter']
        assert actual.reimbursed_status == e['reimbursed_status']


def _assert_recruits_does_not_exist(not_expected):
    for ne in not_expected:
        if ne['processing_id'] is not None:
            actual = Recruit.query.filter_by(
                processing_id=ne['processing_id'],
            ).one_or_none()
        else:
            actual = Recruit.query.filter_by(
                civicrm_case_id=ne['civicrm_case_id'],
            ).one_or_none()

        assert actual is None
