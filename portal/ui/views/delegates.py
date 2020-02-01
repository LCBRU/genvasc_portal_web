import datetime
from flask import render_template, request
from flask_security import login_required
from flask_weasyprint import HTML, render_pdf
from .. import blueprint
from portal.models import Practice, Delegate
from ..forms import SearchForm
from portal.helpers import must_exist


@blueprint.route('/practices/<string:code>/delegates')
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
@login_required
@must_exist(
    model=Practice,
    field=Practice.code,
    request_field='code',
    error_redirect='practices_index',
    message="Practice is not registered"
)
def delegates_pdf(code):
    practice = Practice.query.filter(
        Practice.code == code).first()

    searchForm = SearchForm(formdata=request.args)

    q = Delegate.query.filter(Delegate.practice_code == code)

    if searchForm.search.data:
        q = q.filter(Delegate.name.like("%{}%".format(searchForm.search.data)))

    delegates = q.order_by(Delegate.instance).all()

    html = render_template('practices/delegates/pdf.html', delegates=delegates, practice=practice, now=datetime.datetime.utcnow())
    return render_pdf(HTML(string=html), download_filename='{}_{}_staff.pdf'.format(
        practice.code,
        practice.practice.name,
    ))
