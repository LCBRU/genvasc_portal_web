import re
import datetime
import csv
import tempfile
import io
from flask import render_template, request, redirect, url_for, flash, make_response
from flask_security import login_required, current_user, roles_required
from sqlalchemy import func
from portal import app, db
from portal.models import *
from portal.forms import *
from portal.helpers import *
from portal.datatypes import *

@app.route('/submissions')
@app.route('/submissions?page=<int:page>')
@login_required
@roles_required('admin')
def submissions_index(page=1):
    q = db.session.query(
        RecruitStatus.invoice_year,
        RecruitStatus.invoice_quarter,
        func.count().label('participants')
    ).join(
        RecruitStatus.recruit
    ).filter(
        RecruitStatus.invoice_year != ''
    ).filter(
        RecruitStatus.invoice_quarter != ''
    ).group_by(
        RecruitStatus.invoice_year,
        RecruitStatus.invoice_quarter
    )

    submissions = (
        q.order_by(
            RecruitStatus.invoice_year,
            RecruitStatus.invoice_quarter
        ).paginate(
            page=page,
            per_page=10,
            error_out=False))

    return render_template('submissions/index.html', submissions=submissions)


@app.route('/submissions/<string:invoice_year>/<string:invoice_quarter>')
@app.route('/submissions/<string:invoice_year>/<string:invoice_quarter>?page=<int:page>')
@login_required
@roles_required('admin')
def submissions_participants(invoice_year, invoice_quarter, page=1):

    q = RecruitStatus.query.join(
        Recruit, RecruitStatus.recruit
    ).join(
        PracticeRegistration, Recruit.practice_registration
    ).filter(
        RecruitStatus.invoice_year == invoice_year
    ).filter(
        RecruitStatus.invoice_quarter == invoice_quarter
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

@app.route('/submissions/<string:invoice_year>/<string:invoice_quarter>/csv')
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
    
    q = RecruitStatus.query.join(
        Recruit, RecruitStatus.recruit
    ).join(
        PracticeRegistration, Recruit.practice_registration
    ).filter(
        RecruitStatus.invoice_year == invoice_year
    ).filter(
        RecruitStatus.invoice_quarter == invoice_quarter
    ).filter(
        RecruitStatus.status != 'Excluded'
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