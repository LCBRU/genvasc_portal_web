import pytest
import uuid
from faker import Faker
from faker.providers import BaseProvider


class FakerProvider(BaseProvider):
    def practice_code(self):
        fake = Faker("en_GB")
        return fake.pystr_format(string_format='?#####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def nhs_number(self):
        fake = Faker("en_GB")
        return fake.pystr_format(string_format='##########')

    def study_id(self):
        fake = Faker("en_GB")
        return fake.pystr_format(string_format='GPt#######')

    def etl_delegate_details(self):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'practice_code': self.practice_code(),
            'instance': 2,
            'name': fake.company(),
            'role': fake.company(),
            'gcp_trained': fake.boolean(),
            'gv_trained': fake.boolean(),
            'on_delegation_log_yn': fake.boolean(),
            'gv_start_del_log': fake.date_object(),
            'gv_end_del_log': fake.date_object(),
            'gv_phone_a': fake.phone_number(),
            'gv_phone_b': fake.phone_number(),
            'contact_email_add': fake.email(),
            'primary_contact_yn': fake.boolean(),
        }

    def etl_practice_details(self, practice_code=None):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'practice_code': practice_code or self.practice_code(),
            'practice_name': fake.company(),
            'ccg': 1,
            'practice_address': fake.street_address(),
            'pract_town': fake.city(),
            'city': fake.city(),
            'county': fake.city(),
            'postcode': fake.postcode(),
            'federation': 1,
            'partners': fake.company(),
            'genvasc_initiated': 1,
            'status': 0,
        }

    def etl_ccg_details(self, id):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'ccg_id': id,
            'name': fake.company(),
        }

    def etl_federation_details(self, id):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'federation_id': id,
            'name': fake.company(),
        }

    def etl_user_details(self):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'practice_code': self.practice_code(),
            'email': fake.email(),
            'current_portal_user_yn': 1,
            'gv_end_del_log': None,
        }

    def etl_area_details(self, id):
        fake = Faker("en_GB")
        return {
            'project_id': id,
            'name': fake.company(),
        }

    def etl_recruit_details_not_processed(self, practice_code=None):
        fake = Faker("en_GB")
        return {
            'processing_id': str(uuid.uuid4()),
            'status': 'Awaiting Processing',
            'nhs_number': self.nhs_number(),
            'study_id': None,
            'practice_code': practice_code or self.practice_code(),
            'first_name': None,
            'last_name': None,
            'date_of_birth': fake.date_between(start_date='-70y', end_date='-40y'),
            'civicrm_contact_id': None,
            'civicrm_case_id': None,
            'processed_date': None,
            'recruited_date': fake.date_between(start_date='-2w', end_date='-1d'),
            'invoice_year': None,
            'invoice_quarter': None,
            'reimbursed_status': None,
        }

    def etl_recruit_details_processed(self, practice_code=None):
        fake = Faker("en_GB")
        return {
            'processing_id': None,
            'status': fake.pystr(min_chars=10, max_chars=20),
            'nhs_number': self.nhs_number(),
            'study_id': self.study_id(),
            'practice_code': practice_code or self.practice_code(),
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'date_of_birth': fake.date_between(start_date='-70y', end_date='-40y'),
            'civicrm_contact_id': fake.pyint(min_value=1000, max_value=9999, step=1),
            'civicrm_case_id': fake.pyint(min_value=1000, max_value=9999, step=1),
            'processed_date': fake.date_between(start_date='-2w', end_date='-1d'),
            'recruited_date': fake.date_between(start_date='-2w', end_date='-1d'),
            'invoice_year': int(fake.year()),
            'invoice_quarter': f'Q{fake.pyint(min_value=1, max_value=4, step=1)}',
            'reimbursed_status': 'Yes',
        }


@pytest.yield_fixture(scope="function")
def faker():
    result = Faker("en_GB")
    result.add_provider(FakerProvider)

    yield result
