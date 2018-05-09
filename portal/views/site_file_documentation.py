from flask import render_template
from flask_security import login_required, roles_required
from portal import app


@app.route('/site_file_documentation', methods=['GET'])
@login_required
def site_file_documentation():
    return render_template('site_file_documentation/index.html')


@app.route('/site_file_documentation_approval', methods=['GET'])
@login_required
def site_file_documentation_approval():
    return render_template('site_file_documentation/approval.html')


@app.route('/site_file_documentation_personnel', methods=['GET'])
@login_required
def site_file_documentation_personnel():
    return render_template('site_file_documentation/personnel.html')


@app.route('/site_file_documentation_sops', methods=['GET'])
@login_required
def site_file_documentation_sops():
    return render_template('site_file_documentation/sops.html')


@app.route('/site_file_documentation_admin', methods=['GET'])
@login_required
def site_file_documentation_admin():
    return render_template('site_file_documentation/admin.html')


@app.route('/site_file_documentation_documents', methods=['GET'])
@login_required
def site_file_documentation_documents():
    return render_template('site_file_documentation/documents.html')


@app.route('/site_file_documentation_study_admin', methods=['GET'])
@roles_required('admin')
@login_required
def site_file_documentation_study_admin():
    return render_template('site_file_documentation/study_admin.html')


@app.route('/site_file_documentation_study_admin_docmail', methods=['GET'])
@roles_required('admin')
@login_required
def site_file_documentation_study_admin_docmail():
    return render_template('site_file_documentation/study_admin_docmail.html')
