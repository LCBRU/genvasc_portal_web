import csv
import io
from flask import render_template, make_response
from flask_security import login_required, roles_required
from sqlalchemy import func
from .. import blueprint
from portal.database import db
from portal.models import (
    Recruit,
    PracticeRegistration,
)


@blueprint.route('/submissions')
@blueprint.route('/submissions?page=<int:page>')
@login_required
@roles_required('admin')
def submissions_index(page=1):
    q = db.session.query(
        Recruit.invoice_year,
        Recruit.invoice_quarter,
        func.count().label('participants')
    ).join(
        Recruit.recruit
    ).filter(
        Recruit.invoice_year != ''
    ).filter(
        Recruit.invoice_quarter != ''
    ).group_by(
        Recruit.invoice_year,
        Recruit.invoice_quarter
    )

    submissions = (
        q.order_by(
            Recruit.invoice_year,
            Recruit.invoice_quarter
        ).paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('submissions/index.html', submissions=submissions)


@blueprint.route('/submissions/<string:invoice_year>/<string:invoice_quarter>')
@blueprint.route('/submissions/<string:invoice_year>/<string:invoice_quarter>?page=<int:page>')
@login_required
@roles_required('admin')
def submissions_participants(invoice_year, invoice_quarter, page=1):

    q = Recruit.query.join(
        Recruit, Recruit.recruit
    ).join(
        PracticeRegistration, Recruit.practice_registration
    ).filter(
        Recruit.invoice_year == invoice_year
    ).filter(
        Recruit.invoice_quarter == invoice_quarter
    )

    participants = (
        q.order_by(
            PracticeRegistration.code,
            Recruit.date_recruited.asc()
        ).paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('submissions/participants.html', page=page, participants=participants, invoice_year=invoice_year, invoice_quarter=invoice_quarter)

@blueprint.route('/submissions/<string:invoice_year>/<string:invoice_quarter>/csv')
@login_required
@roles_required('admin')
def submissions_csv(invoice_year, invoice_quarter):

    COL_RECRUITED_DATE = 'Study Entry Date'
    COL_STATUS = 'Status'
    COL_PATIENT_ID = 'Patient ID'
    COL_PRACTICE_CODE = 'Practice Code'
    COL_PRACTICE_NAME = 'Practice Name'
    COL_PRACTICE_ADDRESS = 'Prcatice Address'
    COL_CCG = 'CCG'

    fieldnames = [
        COL_RECRUITED_DATE,
        COL_STATUS,
        COL_PATIENT_ID,
        COL_PRACTICE_CODE,
        COL_PRACTICE_NAME,
        COL_PRACTICE_ADDRESS,
        COL_CCG
    ]

    si = io.StringIO()

    output = csv.DictWriter(
        si,
        fieldnames=fieldnames,
        quoting=csv.QUOTE_NONNUMERIC
    )

    output.writeheader()
    
    q = Recruit.query.join(
        Recruit, Recruit.recruit
    ).join(
        PracticeRegistration, Recruit.practice_registration
    ).filter(
        Recruit.invoice_year == invoice_year
    ).filter(
        Recruit.invoice_quarter == invoice_quarter
    ).filter(
        Recruit.status != 'Excluded'
    )

    participants = q.order_by(
            PracticeRegistration.code,
            Recruit.date_recruited.asc()
        ).all()

    for p in participants:
        output.writerow({
            COL_RECRUITED_DATE: p.recruit.date_recruited,
            COL_STATUS: p.status,
            COL_PATIENT_ID: p.study_id,
            COL_PRACTICE_CODE: p.recruit.practice_registration.code,
            COL_PRACTICE_NAME: p.recruit.practice_registration.practice.name,
            COL_PRACTICE_ADDRESS: p.recruit.practice_registration.practice.address,
            COL_CCG: p.recruit.practice_registration.practice.ccg_name
    })

    resp = make_response(si.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=Genvasc_Submissions_{}{}.csv".format(invoice_year, invoice_quarter)
    resp.headers["Content-type"] = "text/csv"
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = 0
    return resp