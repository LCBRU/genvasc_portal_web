import re
import traceback
from datetime import datetime, date
from dateutil.parser import parse
from portal.emailing import email
from flask import current_app


class ReverseProxied(object):
    '''Wrap the application in this middleware and configure the
    front-end server to add these headers, to let you quietly bind
    this to a URL other than / and to an HTTP scheme that is
    different than what is used locally.

    In nginx:
    location /myprefix {
        proxy_pass http://192.168.0.1:5001;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Scheme $scheme;
        proxy_set_header X-Script-Name /myprefix;
        }

    :param app: the WSGI application
    '''
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        script_name = environ.get('HTTP_X_SCRIPT_NAME', '')
        if script_name:
            environ['SCRIPT_NAME'] = script_name
            path_info = environ['PATH_INFO']
            if path_info.startswith(script_name):
                environ['PATH_INFO'] = path_info[len(script_name):]

        scheme = environ.get('HTTP_X_SCHEME', '')
        if scheme:
            environ['wsgi.url_scheme'] = scheme

        server = environ.get('HTTP_X_FORWARDED_SERVER', '')
        if server:
            environ['HTTP_HOST'] = server

        return self.app(environ, start_response)


def log_exception(e):
    print(traceback.format_exc())
    current_app.logger.error(traceback.format_exc())
    email(
        subject=current_app.config["ERROR_EMAIL_SUBJECT"],
        message=traceback.format_exc(),
        recipients=current_app.config["ADMIN_EMAIL_ADDRESS"].split(";"),
    )


def parse_date(value):
    if not value:
        return None

    if isinstance(value, date) or isinstance(value, datetime):
        return value

    ansi_match = re.fullmatch(r'(?P<year>\d{4})[\\ -]?(?P<month>\d{2})[\\ -]?(?P<day>\d{2})(?:[ T]\d{2}:\d{2}:\d{2})?(?:\.\d+)?(?:[+-]\d{2}:\d{2})?', value)

    if ansi_match:
        return datetime(
            int(ansi_match.group('year')),
            int(ansi_match.group('month')),
            int(ansi_match.group('day')),
        )

    try:
        parsed_date = parse(value, dayfirst=True)
    except ValueError:
        return None

    return parsed_date
