import pytest
from faker import Faker
from faker.providers import BaseProvider


class FakerProvider(BaseProvider):
    def etl_practice_code(self):
        fake = Faker("en_GB")
        return fake.pystr_format(string_format='?#####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def etl_delegate_details(self):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'practice_code': self.etl_practice_code(),
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

    def etl_practice_details(self):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'practice_code': self.etl_practice_code(),
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
            'practice_code': self.etl_practice_code(),
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


@pytest.yield_fixture(scope="function")
def faker():
    result = Faker("en_GB")
    result.add_provider(FakerProvider)

    yield result
