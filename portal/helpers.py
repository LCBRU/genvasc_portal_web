from portal import app
from functools import wraps
from flask import request, render_template, flash, redirect, url_for
from urllib.parse import urlparse, urljoin


@app.template_filter('yes_no')
def yesno_format(value):
    if value is None:
        return ''
    if value:
        return 'Yes'
    else:
        return 'No'


@app.template_filter('datetime_format')
def datetime_format(value):
    if value:
        return value.strftime('%c')
    else:
        return ''


@app.template_filter('date_format')
def date_format(value):
    if value:
        return value.strftime('%-d %b %Y')
    else:
        return ''


@app.template_filter('blank_if_none')
def blank_if_none(value):
    return value or ''


@app.template_filter('default_if_none')
def default_if_none(value, default):
    return value or default


@app.template_filter('currency')
def currency(value):
    if value:
        return '£{:.2f}'.format(value)
    else:
        return ''


def templated(template=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            template_name = template
            if template_name is None:
                template_name = request.endpoint \
                    .replace('.', '/') + '.html'
            ctx = f(*args, **kwargs)
            if ctx is None:
                ctx = {}
            elif not isinstance(ctx, dict):
                return ctx
            return render_template(template_name, **ctx)
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
