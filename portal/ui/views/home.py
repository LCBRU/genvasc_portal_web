from flask import render_template, redirect, url_for, session
from flask_security import current_user, login_user
from portal.models import User
from .. import blueprint

@blueprint.route('/', methods=['GET'])
def index():
	return redirect(url_for('ui.practices_index'))

@blueprint.route('/help', methods=['GET'])
def help():
	return render_template('help.html')
