import re, datetime
from flask import render_template, request, redirect, url_for, flash
from flask_security import login_required, current_user
from portal import app, db
from portal.models import *
from portal.forms import *
from portal.helpers import *
from portal.datatypes import *
from sqlalchemy import func
from flask_weasyprint import HTML, render_pdf

@app.route('/practices/<string:code>/reimbursements')
@app.route('/practices/<string:code>/reimbursements?page=<int:page>')
@login_required
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_index(code, page=1):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    q = db.session.query(
        RecruitStatus.invoice_year,
        RecruitStatus.invoice_quarter,
        func.count().label('participants')
    ).join(
        RecruitStatus.recruit
    ).join(
        Recruit.practice_registration
    ).filter(
        PracticeRegistration.code == code
    ).filter(
        RecruitStatus.invoice_year != ''
    ).filter(
        RecruitStatus.invoice_quarter != ''
    ).group_by(
        RecruitStatus.invoice_year,
        RecruitStatus.invoice_quarter
    )

    reimbursements = (
        q.order_by(
            RecruitStatus.invoice_year,
            RecruitStatus.invoice_quarter
        ).paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('practices/reimbursements/index.html', reimbursements=reimbursements, practice_registration=practice_registration)

@app.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>')
@app.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>?page=<int:page>')
@login_required
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_participants(code, invoice_year, invoice_quarter, page=1):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    q = RecruitStatus.query.join(
        Recruit, RecruitStatus.recruit
    ).join(
        PracticeRegistration, Recruit.practice_registration
    ).filter(
        PracticeRegistration.code == code
    ).filter(
        RecruitStatus.invoice_year == invoice_year
    ).filter(
        RecruitStatus.invoice_quarter == invoice_quarter
    )

    participants = (
        q.order_by(Recruit.date_recruited.asc())
         .paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('practices/reimbursements/participants.html', page=page, participants=participants, practice_registration=practice_registration, invoice_year=invoice_year, invoice_quarter=invoice_quarter)

@app.route('/practices/<string:code>/reimbursements/<string:invoice_year>/<string:invoice_quarter>/pdf')
@login_required
@must_exist(model=PracticeRegistration, field=PracticeRegistration.code, request_field='code', error_redirect='practices_index', message="Practice is not registered")
def reimbursements_pdf(code, invoice_year, invoice_quarter):
    practice_registration = PracticeRegistration.query.filter(PracticeRegistration.code == code).first()

    q = RecruitStatus.query.join(
        Recruit, RecruitStatus.recruit
    ).join(
        PracticeRegistration, Recruit.practice_registration
    ).filter(
        PracticeRegistration.code == code
    ).filter(
        RecruitStatus.invoice_year == invoice_year
    ).filter(
        RecruitStatus.invoice_quarter == invoice_quarter
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