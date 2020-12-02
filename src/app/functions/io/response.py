from flask import jsonify, request, g

from app.constants import ALLOWED_STATUS_FOR_DETAILS, IMPACTED_ENTITIES
from app.functions import REST_VERSION, isProdEnvironment
from app.functions.base.date import convert_date_to_string, now
from app.functions.base.json import empty_json_object, empty_json_array
from app.functions.io.request import request_parameters
from app.functions.logging.logger import error
from app.functions.logging.logstash import log_stash


def make_json_response(json_response, status):
    if "status" not in json_response:
        json_response['status'] = status
    add_server_parameters(json_response)
    response = jsonify(json_response), status, {'Content-Type': 'application/json; charset=utf-8'}
    log_stash(json_response)
    return response


def make_json_redirect(json_response, status, location):
    if "status" not in json_response:
        json_response['status'] = status
    add_server_parameters(json_response)
    response = jsonify(json_response), status, {'Content-Type': 'application/json; charset=utf-8', 'Location': location}
    log_stash(json_response)
    return response


def add_server_parameters(json):
    json['version'] = REST_VERSION
    json['host'] = request.host
    json['returned'] = convert_date_to_string(now())


def add_system_parameters(json, detail, status, title):
    json['status'] = status
    json['title'] = title
    if not isProdEnvironment or status in ALLOWED_STATUS_FOR_DETAILS:
        json['detail'] = detail


def add_entity_details(json_success):
    body = request_parameters()
    if IMPACTED_ENTITIES in body:
        json_success[IMPACTED_ENTITIES] = body[IMPACTED_ENTITIES]


def add_impacted_entity(entity_id, entity_type, json_body):
    type_name = (entity_type + 's').lower()
    type_name = 'addresses' if type_name == 'addresss' else type_name
    entities = json_body[IMPACTED_ENTITIES]
    if type_name not in entities:
        entities[type_name] = empty_json_array()
    if entity_id not in entities[type_name]:
        entities[type_name].append(entity_id)


def fault(detail, error_code, status, title, entity_type=None, instance=None, action=None):
    json_fault = empty_json_object()
    json_fault['error_code'] = error_code
    add_system_parameters(json_fault, detail, status, title)
    parameters = request_parameters()
    if entity_type is None:
        entity_type = parameters.get('type')
    if instance is None:
        instance = parameters.get('instance')
    if action is None:
        action = parameters.get('action')
    if entity_type is not None:
        json_fault['type'] = entity_type
    if instance is not None:
        json_fault['instance'] = instance
    if action is not None:
        json_fault['action'] = action
    error('json.fault: %s, %s', status, json_fault)
    if "fault" in g:
        json_ext_fault = g.pop('fault')
        json_fault['fault'] = json_ext_fault
    return make_json_response(json_fault, status)


def success(detail='Success', status=200, title='Success', entity_type=None, instance=None, action=None,
            post_function=None):
    json_success = make_success(detail, status, title, entity_type, instance, action, post_function)
    return make_json_response(json_success, status)


def make_success(detail='Success', status=200, title='Success', entity_type=None, instance=None, action=None,
                 post_function=None):
    json_success = empty_json_object()
    add_system_parameters(json_success, detail, status, title)
    add_entity_details(json_success)
    if entity_type is not None:
        json_success['type'] = entity_type
    if "delete" == action:
        if instance is not None:
            json_success['instance'] = instance
        json_success['action'] = action
    if post_function is not None:
        post_function(json_success)
    return json_success
