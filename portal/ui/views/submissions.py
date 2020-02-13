import csv
import io
from flask import render_template, make_response
from flask_security import login_required, current_user
from sqlalchemy import func
from .. import blueprint
from ..decorators import is_super_user
from portal.database import db
from portal.models import (
    Recruit,
    Practice,
)


@blueprint.route('/submissions')
@blueprint.route('/submissions?page=<int:page>')
@login_required
@is_super_user()
def submissions_index(page=1):
    q = db.session.query(
        Recruit.invoice_year,
        Recruit.invoice_quarter,
        func.count().label('participants')
    ).filter(
        Recruit.invoice_year != ''
    ).filter(
        Recruit.invoice_quarter != ''
    ).filter(
        Recruit.practice_code.in_(p.code for p in current_user.all_practices)
    ).group_by(
        Recruit.invoice_year,
        Recruit.invoice_quarter
    )

    submissions = (
        q.order_by(
            Recruit.invoice_year.desc(),
            Recruit.invoice_quarter.desc()
        ).paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('submissions/index.html', submissions=submissions)


@blueprint.route('/submissions/<string:invoice_year>/<string:invoice_quarter>')
@blueprint.route('/submissions/<string:invoice_year>/<string:invoice_quarter>?page=<int:page>')
@login_required
@is_super_user()
def submissions_participants(invoice_year, invoice_quarter, page=1):

    q = Recruit.query.join(
        Practice, Recruit.practice
    ).filter(
        Recruit.invoice_year == invoice_year
    ).filter(
        Recruit.invoice_quarter == invoice_quarter
    ).filter(
        Recruit.practice_code.in_(p.code for p in current_user.all_practices)
    )

    participants = (
        q.order_by(
            Practice.code,
            Recruit.date_recruited.asc()
        ).paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('submissions/participants.html', page=page, participants=participants, invoice_year=invoice_year, invoice_quarter=invoice_quarter)


@blueprint.route('/submissions/<string:invoice_year>/<string:invoice_quarter>/csv')
@login_required
@is_super_user()
def submissions_csv(invoice_year, invoice_quarter):

    COL_RECRUITED_DATE = 'Study Entry Date'
    COL_STATUS = 'Status'
    COL_PATIENT_ID = 'Patient ID'
    COL_PRACTICE_CODE = 'Practice Code'
    COL_PRACTICE_NAME = 'Practice Name'
    COL_PRACTICE_ADDRESS = 'Practice Address'
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
        Practice, Recruit.practice
    ).filter(
        Recruit.invoice_year == invoice_year
    ).filter(
        Recruit.invoice_quarter == invoice_quarter
    ).filter(
        Recruit.status != 'Excluded'
    ).filter(
        Recruit.practice_code.in_(p.code for p in current_user.all_practices)
    )

    participants = q.order_by(
            Practice.code,
            Recruit.date_recruited.asc()
        ).all()

    for p in participants:
        output.writerow({
            COL_RECRUITED_DATE: p.date_recruited,
            COL_STATUS: p.status,
            COL_PATIENT_ID: p.study_id,
            COL_PRACTICE_CODE: p.practice.code,
            COL_PRACTICE_NAME: p.practice.name,
            COL_PRACTICE_ADDRESS: p.practice.full_address,
            COL_CCG: p.practice.ccg_name
    })

    resp = make_response(si.getvalue())
    resp.headers["Content-Disposition"] = "attachment; filename=Genvasc_Submissions_{}{}.csv".format(invoice_year, invoice_quarter)
    resp.headers["Content-type"] = "text/csv"
    resp.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = 0
    return resp