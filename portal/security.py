from portal import app, user_datastore
from portal.models import Role


@app.before_first_request
def init_security():
    user_datastore.find_or_create_role(
        name=Role.ADMIN_ROLENAME,
        description='Administration')
