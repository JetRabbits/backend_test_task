import time

from flask import request, g, make_response, render_template

from app.functions import app, isDebugMode
from app.functions.base.date import now
from app.functions.base.json import json_to_string, empty_json_object, to_json
from app.functions.base.string import replace
from app.functions.logging.logger import exception
from app.functions.utils.jwt import decode_jwt_token


def request_parameters(to_dict=False):
    parameters = {}
    try:
        if request.method == 'POST' and request.get_json() is not None:
            parameters = request.get_json()
        else:
            parameters = to_json(request.args)
        save_request(parameters)
    except Exception as e:
        exception(e)
    return parameters


def save_request(parameters):
    if "request_parameters" not in g:
        g.request_parameters = json_to_string(parameters)
    if "token" not in g and "token" in parameters:
        g.token = parameters.get('token')


def security_path(path=None):
    if path is None:
        request_path = replace(
            replace(replace(replace(request.path.replace('/search', ''), '/update', ''), '/add', ''), '/test', ''),
            '/all', '')
        return request_path if request_path.find('-') == -1 else request_path[0: request_path.rfind('/')]
    else:
        return path


def get_ip():
    real_client_ip = request.headers.getlist("X-Forwarded-For")
    return real_client_ip[0] if len(real_client_ip) > 0 else request.remote_addr


def get_mobile_version():
    mobile_version = 'undefined'
    args = request.args
    if "mobile_version" in args:
        mobile_version = args.get('mobile_version')
    return mobile_version


def get_platform():
    platform = 'undefined'
    args = request.args
    if "platform" in args:
        platform = args.get('platform')
    return platform


def init_body():
    body = empty_json_object()
    body['instance'] = ''
    return body


def pop_token():
    parameters = request_parameters()
    if "token" in parameters and request.method == 'POST':
        parameters.pop('token')


@app.after_request
def after_request(response):
    try:
        response = run_debug_toolbar_for_json_if_needed(response)
    except Exception as e:
        exception('after_request.exception: %s', e)
    finally:
        return response


@app.before_request
def before_request():
    if "request.start_time" not in g:
        g.requested = now()
        g.requested_ms = int(round(time.time() * 1000))


def run_debug_toolbar_for_json_if_needed(response):
    is_json = response.mimetype == "application/json"
    if isDebugMode and is_json and response.status_code != 401 and request.method == 'GET':
        response.direct_passthrough = False
        args = dict(response=response.data.decode("utf-8"), http_code=response.status)
        html_wrapped_response = make_response(render_template("wrap_json.html", **args), response.status_code)
        response = app.extensions['debugtoolbar'].process_response(html_wrapped_response)
    return response


def extract_private_token():
    token1 = g.token if "token" in g else request_parameters().get('token')
    payload = decode_jwt_token(token1, app.config['SECRET_KEY'])
    token2 = payload['token']
    return token2