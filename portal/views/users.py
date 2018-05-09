from flask import render_template, request, redirect, url_for, flash
from flask_security import login_required
from flask_security.utils import logout_user
from portal import app, db
from portal.models import *
from portal.forms import *
from portal.helpers import *

@app.route('/users_logout/')
@login_required
def users_logout():
    logout_user()
    return redirect(url_for("index"))
    