from flask import render_template, request, redirect, url_for
from flask_security import login_required, current_user
from portal import app
from sqlalchemy import or_
from portal.models import *
from portal.forms import *
from portal.helpers import *


@app.route('/practices/')
@login_required
def practices_index():
    searchForm = SearchForm(formdata=request.args)

    q = PracticeRegistration.query.join(
        Practice,
        PracticeRegistration.practice
    )

    if (not current_user.is_admin()):
        q = q.filter(
            PracticeRegistration.id.in_(
                [p.id for p in current_user.practices]))

    if searchForm.search.data:
        q = q.filter(
            or_(
                Practice.name.like("%{}%".format(searchForm.search.data)),
                Practice.code == searchForm.search.data))

    registrations = (
        q.order_by(Practice.name.asc())
         .paginate(
            page=searchForm.page.data,
            per_page=10,
            error_out=False))

    if registrations.total == 1:
        return redirect(url_for(
            'recruits_index',
            code=registrations.items[0].code))

    return render_template(
        'practices/index.html',
        registrations=registrations,
        searchForm=searchForm)
