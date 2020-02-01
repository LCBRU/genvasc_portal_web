from flask import render_template, request, redirect, url_for
from flask_security import login_required, current_user
from .. import blueprint
from sqlalchemy import or_
from portal.models import PracticeRegistration, Practice
from ..forms import SearchForm


@blueprint.route('/practices/')
@login_required
def practices_index():
    searchForm = SearchForm(formdata=request.args)

    q = Practice.query

    if (not current_user.is_admin()):
        q = q.filter(Practice.code.in_(
            [p.code for p in current_user.practices],
        ))

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
