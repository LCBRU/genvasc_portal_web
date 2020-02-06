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
)
from .. import blueprint
from ..forms import SearchForm
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

    searchForm = SearchForm(formdata = request.args)

    q = Recruit.query.join(Practice, Recruit.practice).filter(Practice.code == code)

    if searchForm.search.data:
        string_in_name = db.session.query(Recruit.id).filter(func.concat(Recruit.first_name, ' ', Recruit.last_name).ilike("%{}%".format(searchForm.search.data)))
        string_in_study_id = db.session.query(Recruit.id).filter(Recruit.study_id.ilike("%{}%".format(searchForm.search.data)))
        q = q.filter(or_(
            Recruit.nhs_number.like("%{}%".format(searchForm.search.data)),
            Recruit.id.in_(string_in_name),
            Recruit.id.in_(string_in_study_id)
            ))

    recruits = (
        q.order_by(Recruit.date_recruited.desc())
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False))

    return render_template('practices/recruits/index.html', recruits=recruits, practice=practice, searchForm=searchForm)

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
    ).join(
        Recruit.practice
    ).filter(
        Practice.code == code
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

    q = Recruit.query.join(
        Practice, Recruit.practice
    ).filter(
        Practice.code == code
    ).filter(
        Recruit.invoice_year == invoice_year
    ).filter(
        Recruit.invoice_quarter == invoice_quarter
    )

    participants = (
        q.order_by(Recruit.date_recruited.asc())
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

    q = Recruit.query.join(
        Practice, Recruit.practice
    ).filter(
        Practice.code == code
    ).filter(
        Recruit.invoice_year == invoice_year
    ).filter(
        Recruit.invoice_quarter == invoice_quarter
    )

    participants = q.order_by(Recruit.date_recruited.asc()).all()

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

    searchForm = SearchForm(formdata=request.args)

    q = Delegate.query.filter(Delegate.practice_code == code)

    if searchForm.search.data:
        q = q.filter(Delegate.name.like("%{}%".format(searchForm.search.data)))

    delegates = (
        q.order_by(Delegate.instance)
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False,
        ))

    return render_template(
        'practices/delegates/index.html',
        delegates=delegates,
        practice=practice,
        searchForm=searchForm,
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

    searchForm = SearchForm(formdata=request.args)

    q = Delegate.query.filter(Delegate.practice_code == code)

    if searchForm.search.data:
        q = q.filter(Delegate.name.like("%{}%".format(searchForm.search.data)))

    delegates = q.order_by(Delegate.instance).all()

    html = render_template('practices/delegates/pdf.html', delegates=delegates, practice=practice, now=datetime.datetime.utcnow())
    return render_pdf(HTML(string=html), download_filename='{}_{}_staff.pdf'.format(
        practice.code,
        practice.name,
    ))
