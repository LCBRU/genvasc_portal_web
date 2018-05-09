import re
from datetime import date

class NhsNumberHelper(object):
    @staticmethod
    def format(value):
        return re.sub('[- ]', '', value)

    @staticmethod
    def is_valid(value):

        formated_value = NhsNumberHelper.format(value)

        # A valid NHS number must be 10 digits long
        if not re.search(r'^[0-9]{10}$', formated_value):
        	return False

        checkcalc = lambda sum: 11 - (sum % 11)

        l = [int(j) * (10 - (i)) for i, j in enumerate(formated_value[:-1])]
        checksum = checkcalc(sum(l)) if checkcalc(sum(l)) != 11 else 0

        return checksum == int(formated_value[9])

class DateHelper(object):
    @staticmethod
    def age_in_years(value):
        return Age.full_years_since(date.today())

    @staticmethod
    def full_years_since(value, since):
        return since.year - value.year - ((since.month, since.day) < (value.month, value.day))
