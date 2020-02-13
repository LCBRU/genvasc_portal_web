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
