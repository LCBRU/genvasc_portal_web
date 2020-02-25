from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField
from wtforms.validators import Length


class FlashingForm(FlaskForm):
    def validate_on_submit(self):
        result = super(FlashingForm, self).validate_on_submit()

        if not result:
            for field, errors in self.errors.items():
                for error in errors:
                    flash(
                        "Error in the {} field - {}".format(
                            getattr(self, field).label.text, error
                        ), 'error')
        return result


class SearchForm(FlashingForm):
    search = StringField('Search', validators=[Length(max=20)])
    page = IntegerField('Page', default=1)


class PracticeSearchForm(SearchForm):
    collabortaion_signed = SelectField('Collaboration Signed', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    has_current_isa = SelectField('Has Current ISA', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    genvasc_initiated = SelectField('GENVASC Initiated', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    status = SelectField('Status', choices=[])
    sort_by = SelectField('Sort By', choices=[
        ('name', 'Name'),
        ('code', 'Code'),
        ('recruits_desc', 'Most Recruits'),
        ('recruits_asc', 'Least Recruits'),
        ('excluded_desc', 'Highest % Excluded'),
        ('excluded_asc', 'Lowest % Excluded'),
        ('withdrawn_desc', 'Highest % Withdrawn'),
        ('withdrawn_asc', 'Lowest % Withdrawn'),
        ('last_recruited_asc', 'Last Recruitment (ascending)'),
        ('last_recruited_desc', 'Last Recruitment (descending)'),
    ])


class DelegateSearchForm(SearchForm):
    end_date_exists = SelectField('Has End Date', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    has_logged_on = SelectField('Has Logged On', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    gcp_trained = SelectField('GCP Trained', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    genvasc_trained = SelectField('GENVASC Trained', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    on_delegation_log = SelectField('On delegation Log', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    primary_contact = SelectField('Primary Contact', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])


class RecruitSearchForm(SearchForm):
    recruited_or_available = SelectField('Recruited or Available', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    excluded = SelectField('Excluded', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    withdrawn = SelectField('Withdrawn', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
    reimbursed = SelectField('Reimbursed', choices=[('', ''), ('true', 'Yes'), ('false', 'No')])
