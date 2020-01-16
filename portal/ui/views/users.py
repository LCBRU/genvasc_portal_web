from flask import redirect, url_for
from flask_security import login_required
from flask_security.utils import logout_user
from .. import blueprint

@blueprint.route('/users_logout/')
@login_required
def users_logout():
    logout_user()
    return redirect(url_for("index"))
    