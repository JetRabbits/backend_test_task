import json

import requests
from werkzeug.exceptions import BadRequest

from app.constants import ID, CLIENT_ROLE, SENSITIVE_DATA_CLASSES, SENSITIVE_DATA_EXCLUDED_FROM_MERGE_CLASSES
from app.functions import REST_GUIDE
from app.functions.base.json import empty_json_object
from app.functions.base.uuid import generate_uuid
from app.functions.crud.bulk_post import merge_entity
from app.functions.io.request import extract_private_token, pop_token
from app.functions.io.response import make_json_response, success
from app.functions.utils.context import session_scope
from app.functions.utils.decorator import auth_required
from app.functions.utils.jwt import build_auth_headers


def get_private_token_url():
    raise BadRequest('not implemented')


def post_private_response(body, url=None):
    private_url = url if url is not None else get_private_token_url()
    auth_headers = build_auth_headers({'id': generate_uuid()}, CLIENT_ROLE)
    body['token'] = extract_private_token()
    response = requests.post(private_url, data=json.dumps(body), headers=auth_headers)
    return response.json(), response.status_code


@auth_required('post')
def post_entities(body, clazz, array_name, setup_function=None, teardown_function=None):
    entity_name = clazz.__name__
    json_array = body[array_name]
    is_sensitive_data = entity_name in SENSITIVE_DATA_CLASSES
    if is_sensitive_data:
        for json_entity in json_array:
            body['action'] = ''
            body['instance'] = ''
            if "id" not in json_entity:
                json_entity[ID] = generate_uuid()
        json_entity, code = post_private_response(body)
        if code != 200 or entity_name in SENSITIVE_DATA_EXCLUDED_FROM_MERGE_CLASSES:
            return make_json_response(json_entity, code)

    with session_scope() as session:
        for json_entity in json_array:
            body['action'] = ''
            body['instance'] = ''
            if is_sensitive_data:
                entity_id = json_entity[ID]
                json_entity = empty_json_object()
                json_entity[ID] = entity_id
            elif setup_function is not None:
                setup_function(json_entity, session)
            merge_entity(clazz, json_entity, body, session)
        pop_token()
    return success('POST /' + array_name, 200, 'Success',
                   REST_GUIDE + entity_name, body['instance'], body['action'], teardown_function)