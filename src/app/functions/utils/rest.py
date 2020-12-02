import time

from flask import g
from sqlalchemy import text

from app.functions import REST_VERSION
from app.functions.base.date import convert_date_to_string, now
from app.functions.base.json import empty_json_object
from app.functions.io.response import make_json_response, success
from app.functions.logging.logger import info
from app.functions.utils.query import first


def get_version():
    json_version = {"version": REST_VERSION}
    return make_json_response(json_version, 200)


def get_health():
    returned_server_time = convert_date_to_string(now())
    query = '''select now() as current_time from dual'''
    returned_database_time = first(text(query))['current_time']
    info("server_time: %s; database_time: %s", returned_server_time, returned_database_time)
    processed = int(round(time.time() * 1000)) - g.requested_ms
    json = empty_json_object()
    json['processed_time_ms'] = processed
    json['returned_server_time'] = returned_server_time
    json['returned_database_time'] = returned_database_time
    return make_json_response(json, 200)