import datetime
from flask import render_template, request, redirect, url_for
from flask_security import login_required, current_user
from flask_weasyprint import HTML, render_pdf
from sqlalchemy import or_, func
from portal.database import db
from portal.models import (
    Delegate,
    Practice,
    Recruit,
    User,
)
from .. import blueprint
from ..forms import SearchForm, DelegateSearchForm, RecruitSearchForm
from ..decorators import assert_practice_user, must_exist


@blueprint.route('/practices/')
@login_required
def practices_index():
    searchForm = SearchForm(formdata=request.args)

    q = Practice.query

    if (not current_user.is_admin):
        q = q.filter(Practice.code.in_(p.code for p in current_user.all_practices))

    if searchForm.search.data:
        q = q.filter(
            or_(
                Practice.name.like("%{}%".format(searchForm.search.data)),
                Practice.street_address.like("%{}%".format(searchForm.search.data)),
                Practice.town.like("%{}%".format(searchForm.search.data)),
                Practice.city.like("%{}%".format(searchForm.search.data)),
                Practice.county.like("%{}%".format(searchForm.search.data)),
                Practice.postcode.like("%{}%".format(searchForm.search.data)),
                Practice.partners.like("%{}%".format(searchForm.search.data)),
                Practice.code == searchForm.search.data),
            )

    practices = (
        q.order_by(Practice.name.asc())
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False))

    if practices.total == 1:
        return redirect(url_for(
            'ui.recruits_index',
            code=practices.items[0].code))

    return render_template(
        'practices/index.html',
        practices=practices,
        searchForm=searchForm,
    )


@blueprint.route('/practices/<string:code>/recruits')
@blueprint.route('/practices/<string:code>')
@assert_practice_user()
@login_required
@must_exist(model=Practice, field=Practice.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def recruits_index(code):
    practice = Practice.query.filter(Practice.code == code).first()

    search_form = RecruitSearchForm(formdata = request.args)

    q = Recruit.query.filter(Recruit.practice_code == code)
    q = filter_equals_by_truefalsenone(q, search_form.excluded, Recruit.status, 'Excluded')

    if search_form.recruited_or_available.data.casefold() == 'true':
        q = q.filter(or_(Recruit.status == 'Recruited', Recruit.status == 'Available for cohort'))
    elif search_form.recruited_or_available.data.casefold() == 'false':
        q = q.filter(Recruit.status != 'Recruited')
        q = q.filter(Recruit.status != 'Available for cohort')

    q = filter_equals_by_truefalsenone(q, search_form.withdrawn, Recruit.status, 'Withdrawn')
    q = filter_isNone_by_truefalsenone(q, search_form.reimbursed, Recruit.invoice_year)

    if search_form.search.data:
        string_in_name = db.session.query(Recruit.civicrm_case_id).filter(func.concat(Recruit.first_name, ' ', Recruit.last_name).ilike("%{}%".format(search_form.search.data)))
        string_in_study_id = db.session.query(Recruit.civicrm_case_id).filter(Recruit.study_id.ilike("%{}%".format(search_form.search.data)))
        q = q.filter(or_(
            Recruit.nhs_number.like("%{}%".format(search_form.search.data)),
            Recruit.civicrm_case_id.in_(string_in_name),
            Recruit.civicrm_case_id.in_(string_in_study_id)
            ))

    recruits = (
        q.order_by(Recruit.recruited_date.desc())
         .paginate(
            page=search_form.page.data,
            per_page=10,
            error_out=False))

    return render_template('practices/recruits/index.html', recruits=recruits, practice=practice, searchForm=search_form)


@blueprint.route('/practices/<string:code>/reimbursements')
@blueprint.route('/practices/<string:code>/reimbursements?page=<int:page>')
@assert_practice_user()
@login_required
@must_exist(model=Practice, field=Practice.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_index(code, page=1):
    practice = Practice.query.filter(Practice.code == code).first()

    q = db.session.query(
        Recruit.invoice_year,
        Recruit.invoice_quarter,
        func.count().label('participants')
    ).filter(
        Recruit.practice_code == code
    ).filter(
        Recruit.invoice_year != ''
    ).filter(
        Recruit.invoice_quarter != ''
    ).group_by(
        Recruit.invoice_year,
        Recruit.invoice_quarter
    )

    reimbursements = (
        q.order_by(
            Recruit.invoice_year,
            Recruit.invoice_quarter
        ).paginate(
            page=page,
            per_page=10,
            error_out=False,
        )
    )

    return render_template('practices/reimbursements/index.html', reimbursements=reimbursements, practice=practice)


@blueprint.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>')
@blueprint.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>?page=<int:page>')
@assert_practice_user()
@login_required
@must_exist(model=Practice, field=Practice.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_participants(code, invoice_year, invoice_quarter, page=1):
    practice = Practice.query.filter(Practice.code == code).first()

    q = Recruit.query.filter(
        Recruit.practice_code == code
    ).filter(
        Recruit.invoice_year == invoice_year
    ).filter(
        Recruit.invoice_quarter == invoice_quarter
    )

    participants = (
        q.order_by(Recruit.recruited_date.asc())
         .paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('practices/reimbursements/participants.html', page=page, participants=participants, practice=practice, invoice_year=invoice_year, invoice_quarter=invoice_quarter)


@blueprint.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>/pdf')
@assert_practice_user()
@login_required
@must_exist(model=Practice, field=Practice.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_pdf(code, invoice_year, invoice_quarter):
    practice = Practice.query.filter(Practice.code == code).first()

    q = Recruit.query.filter(
        Recruit.practice_code == code
    ).filter(
        Recruit.invoice_year == invoice_year
    ).filter(
        Recruit.invoice_quarter == invoice_quarter
    )

    participants = q.order_by(Recruit.recruited_date.asc()).all()

    totals = {
        'count': len(participants),
        'submitted': sum(1 for i in participants if i.reimbursed_status == 'Yes'),
        'excluded': sum(1 for i in participants if i.status == 'Excluded'),
        'value': sum(1 for i in participants if i.reimbursed_status == 'Yes') * 16,
    }

    html = render_template('practices/reimbursements/pdf.html', participants=participants, practice=practice, invoice_year=invoice_year, invoice_quarter=invoice_quarter, totals=totals, now=datetime.datetime.utcnow())
    return render_pdf(HTML(string=html))


@blueprint.route('/practices/<string:code>/delegates')
@assert_practice_user()
@login_required
@must_exist(
    model=Practice,
    field=Practice.code,
    request_field='code',
    error_redirect='practices_index',
    message="Practice is not registered")
def delegates_index(code):
    practice = Practice.query.filter(Practice.code == code).first()

    search_form = DelegateSearchForm(formdata=request.args)

    q = delegate_search_query(search_form, code)

    delegates = (
        q.order_by(Delegate.instance)
         .paginate(
            page=search_form.page.data,
            per_page=10,
            error_out=False,
        ))

    return render_template(
        'practices/delegates/index.html',
        delegates=delegates,
        practice=practice,
        searchForm=search_form,
    )


@blueprint.route('/practices/<string:code>/delegates/pdf')
@assert_practice_user()
@login_required
@must_exist(
    model=Practice,
    field=Practice.code,
    request_field='code',
    error_redirect='practices_index',
    message="Practice is not registered"
)
def delegates_pdf(code):
    practice = Practice.query.filter(Practice.code == code).first()
    delegates = Delegate.query.filter(Delegate.practice_code == code).order_by(Delegate.instance).all()

    html = render_template('practices/delegates/pdf.html', delegates=delegates, practice=practice, now=datetime.datetime.utcnow())
    return render_pdf(HTML(string=html), download_filename='{}_{}_staff.pdf'.format(
        practice.code,
        practice.name,
    ))


def delegate_search_query(search_form, code):
    q = Delegate.query.filter(Delegate.practice_code == code).outerjoin(User)

    if search_form.search.data:
        q = q.filter(Delegate.name.like("%{}%".format(search_form.search.data)))

    q = filter_isNone_by_truefalsenone(q, search_form.end_date_exists, Delegate.gv_end_del_log)
    q = filter_isNone_by_truefalsenone(q, search_form.has_logged_on, User.last_login_at)
    q = filter_boolean_by_truefalsenone(q, search_form.gcp_trained, Delegate.gcp_trained)
    q = filter_boolean_by_truefalsenone(q, search_form.genvasc_trained, Delegate.gv_trained)
    q = filter_boolean_by_truefalsenone(q, search_form.on_delegation_log, Delegate.on_delegation_log_yn)
    q = filter_boolean_by_truefalsenone(q, search_form.primary_contact, Delegate.primary_contact_yn)

    return q


def filter_equals_by_truefalsenone(query, form_field, model_field, value):
    if form_field.data.casefold() == 'true':
        return query.filter(model_field == value)
    elif form_field.data.casefold() == 'false':
        return query.filter(model_field != value)
    else:
        return query


def filter_isNone_by_truefalsenone(query, form_field, model_field):
    if form_field.data.casefold() == 'true':
        return query.filter(model_field != None)
    elif form_field.data.casefold() == 'false':
        return query.filter(model_field == None)
    else:
        return query


def filter_boolean_by_truefalsenone(query, form_field, model_field):
    if form_field.data.casefold() == 'true':
        return query.filter(model_field == True)
    elif form_field.data.casefold() == 'false':
        return query.filter(model_field == False or model_field == None)
    else:
        return query
