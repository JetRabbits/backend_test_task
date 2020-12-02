import logging.config
import os
import pydoc
import time

from flask import request, g

from app.constants import UNDEFINED, USER_SESSION_CLASS
from app.functions import REST_VERSION
from app.functions.base.date import convert_date_with_ms_to_string, now
from app.functions.base.json import empty_json_object, json_to_string, to_json
from app.functions.io.request import get_ip
from app.functions.io.request import request_parameters, security_path
from app.functions.logging.logger import exception
from app.functions.utils.context import session_scope


def log_stash(response):
    try:
        is_log_stash_mode = (os.environ.get("LOGTASH_MODE") == 'True') or False
        if is_log_stash_mode:
            logger = logging.getLogger('logstash')
            extra = build_log_stash_extra(response)
            current_time = convert_date_with_ms_to_string(now())
            logger.info(current_time, extra=extra)
    except Exception as e:
        exception(e)


def build_log_stash_extra(response):
    request_parameters()
    extra = empty_json_object()
    build_base_info(extra)
    build_request_info(extra)
    build_response_info(extra, response)
    build_data_info(extra)
    build_session_info(extra)
    return extra


def build_base_info(extra):
    extra['path'] = security_path()
    extra['method'] = request.method
    extra['client_ip'] = get_ip()
    extra['host'] = request.host
    extra['rest'] = REST_VERSION
    extra['pid'] = os.getpid()


def build_session_info(extra):
    user_session = get_user_session()
    extra['user_session'] = empty_json_object()
    extra['user_session']['raw'] = 'user_session.raw:\n' + json_to_string(user_session)
    extra['user_id'] = g.user_id if "user_id" in g else \
        user_session.get('person_id') if "person_id" in user_session else UNDEFINED
    if "platform" in user_session:
        extra['user_session']['platform'] = user_session['platform']
    if "sender" in g:
        extra['sender'] = g.sender
    if "login" in g:
        extra['login'] = g.login


def build_data_info(extra):
    if "data" in g:
        extra['data'] = json_to_string(g.data)


def build_response_info(extra, response):
    json_response = json_to_string(response)
    extra['response'] = empty_json_object()
    extra['response']['raw'] = 'response.raw:\n' + json_response[:10000]
    extra['response']['length'] = len(json_response)
    extra['response']['returned'] = convert_date_with_ms_to_string(now())
    if "status" in response:
        extra['response']['status'] = response['status']
    if "error_code" in json_response:
        extra['response']['error_code'] = response['error_code']


def build_request_info(extra):
    extra['request'] = empty_json_object()
    extra['request']['full_path'] = request.full_path
    if "request_parameters" in g:
        extra['request']['raw'] = 'request.raw:\n' + g.request_parameters[:10000]
        extra['request']['length'] = len(g.request_parameters)
    if "requested" in g:
        extra['request']['requested'] = convert_date_with_ms_to_string(g.requested)
    if "requested_ms" in g:
        extra['request']['processed'] = int(round(time.time() * 1000)) - g.requested_ms


def get_user_session():
    ip = get_ip()
    token = g.token if "token" in g else ''
    clazz = pydoc.locate(USER_SESSION_CLASS)
    with session_scope() as session:
        user_session = session.query(clazz).filter_by(token=token, ip=ip).first()
        return to_json(user_session) if user_session is not None else empty_json_object()