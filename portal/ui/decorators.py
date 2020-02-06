from functools import wraps
from flask import flash, abort, request, redirect
from flask_login import current_user
from portal.models import Practice
from portal.helpers import redirect_back_url


def assert_practice_user():
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            practice = Practice.query.get_or_404(kwargs.get('code'))

            if practice not in current_user.all_practices:
                abort(403)

            return f(*args, **kwargs)

        return decorated_function
    return decorator


def must_exist(
    model,
    field,
    request_field,
    error_redirect=None,
    message=u'The value does not exist'
):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            count = model.query.filter(
                field == request.view_args.get(request_field)).count()

            if count == 0:
                flash("{0}: ({1} = '{2}')".format(
                    message,
                    request_field,
                    request.view_args.get(request_field)), 'error')
                return redirect(redirect_back_url(error_redirect))

            return f(*args, **kwargs)

        return decorated_function
    return decorator


