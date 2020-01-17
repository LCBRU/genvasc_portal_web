import pytest
from faker import Faker
from faker.providers import BaseProvider


class FakerProvider(BaseProvider):
    def etl_practice_code(self):
        fake = Faker("en_GB")
        return fake.pystr_format(string_format='?#####', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')

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


@pytest.yield_fixture(scope="function")
def faker():
    result = Faker("en_GB")
    result.add_provider(FakerProvider)

    yield result
