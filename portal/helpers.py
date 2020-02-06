from flask import request, url_for
from urllib.parse import urlparse, urljoin


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
