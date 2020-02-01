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

    def etl_practice_details(self, practice_code=None):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'code': practice_code or self.practice_code(),
            'name': fake.company(),
            'ccg': 1,
            'street_address': fake.street_address(),
            'town': fake.city(),
            'city': fake.city(),
            'county': fake.city(),
            'postcode': fake.postcode(),
            'federation': 1,
            'partners': fake.company(),
            'genvasc_initiated': 1,
            'status': 0,
        }

    def etl_user_details(self, is_imported=False):
        fake = Faker("en_GB")
        return {
            'project_id': 1,
            'practice_code': self.practice_code(),
            'email': fake.email(),
            'current_portal_user_yn': 1,
            'gv_end_del_log': None,
            'is_imported': is_imported,
        }


@pytest.yield_fixture(scope="function")
def faker():
    result = Faker("en_GB")
    result.add_provider(FakerProvider)

    yield result
