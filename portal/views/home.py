from flask import render_template, request, redirect, url_for, flash
from portal import app

@app.route('/', methods=['GET'])
def index():
	return redirect(url_for('practices_index'))

@app.route('/help', methods=['GET'])
def help():
	return render_template('help.html')
