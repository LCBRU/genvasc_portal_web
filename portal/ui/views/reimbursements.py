import datetime
from flask import render_template
from flask_security import login_required
from .. import blueprint
from portal.database import db
from portal.models import (
    PracticeRegistration,
    Recruit,
)
from portal.helpers import must_exist
from sqlalchemy import func
from flask_weasyprint import HTML, render_pdf

@blueprint.route('/practices/<string:code>/reimbursements')
@blueprint.route('/practices/<string:code>/reimbursements?page=<int:page>')
@login_required
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_index(code, page=1):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    q = db.session.query(
        Recruit.invoice_year,
        Recruit.invoice_quarter,
        func.count().label('participants')
    ).join(
        Recruit.recruit
    ).join(
        Recruit.practice_registration
    ).filter(
        PracticeRegistration.code == code
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
            error_out=False))

    return render_template('practices/reimbursements/index.html', reimbursements=reimbursements, practice_registration=practice_registration)


@blueprint.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>')
@blueprint.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>?page=<int:page>')
@login_required
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_participants(code, invoice_year, invoice_quarter, page=1):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    q = Recruit.query.join(
        Recruit, Recruit.recruit
    ).join(
        PracticeRegistration, Recruit.practice_registration
    ).filter(
        PracticeRegistration.code == code
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

    return render_template('practices/reimbursements/participants.html', page=page, participants=participants, practice_registration=practice_registration, invoice_year=invoice_year, invoice_quarter=invoice_quarter)


@blueprint.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>/pdf')
@login_required
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_pdf(code, invoice_year, invoice_quarter):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    q = Recruit.query.join(
        Recruit, Recruit.recruit
    ).join(
        PracticeRegistration, Recruit.practice_registration
    ).filter(
        PracticeRegistration.code == code
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

    html = render_template('practices/reimbursements/pdf.html', participants=participants, practice_registration=practice_registration, invoice_year=invoice_year, invoice_quarter=invoice_quarter, totals=totals, now=datetime.datetime.utcnow())
    return render_pdf(HTML(string=html))