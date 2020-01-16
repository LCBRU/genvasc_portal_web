from functools import wraps
from flask import request, flash, redirect, url_for
from urllib.parse import urlparse, urljoin


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


def redirect_back_url(default='index'):
    return safe_url(request.args.get('next')) or \
        safe_url(request.referrer) or \
        url_for(default)


def safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    if test_url.scheme in ('http', 'https') and \
            ref_url.netloc == test_url.netloc:
        return target
