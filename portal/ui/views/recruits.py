from flask import render_template, request
from flask_security import login_required
from .. import blueprint
from portal.database import db
from portal.models import Recruit, Practice
from ..forms import SearchForm
from portal.helpers import must_exist
from sqlalchemy import or_, func


@blueprint.route('/practices/<string:code>/recruits')
@blueprint.route('/practices/<string:code>')
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
