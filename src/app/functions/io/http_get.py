import uuid

import requests
from werkzeug.exceptions import BadRequest

from app.constants import CLIENT_ROLE, SENSITIVE_DATA_CLASSES
from app.functions.base.uuid import generate_uuid
from app.functions.crud.bulk_get import get_entities, get_sensitive_data_by_ids
from app.functions.io.response import make_json_response
from app.functions.utils.context import session_scope
from app.functions.utils.decorator import auth_required
from app.functions.utils.jwt import build_auth_headers


def get_private_token_url():
    raise BadRequest('not implemented')


def get_private_response(private_url=None):
    private_url = private_url if private_url is not None else get_private_token_url()
    auth_headers = build_auth_headers({'id': generate_uuid()}, CLIENT_ROLE)
    response = requests.get(private_url, headers=auth_headers)
    return response.json(), response.status_code


def get_sensitive_data(array_name, get_relation_entity_function=None):
    json, code = get_private_response()
    if code == 200 and get_relation_entity_function is not None:
        json_array = json[array_name]
        get_relation_entity_function(json_array)
    return make_json_response(json, code)


@auth_required('get_all')
def get_all(clazz, array_name, get_relation_entity_function=None):
    entity_name = clazz.__name__
    if entity_name in SENSITIVE_DATA_CLASSES:
        return get_sensitive_data(array_name, get_relation_entity_function)
    else:
        with session_scope() as session:
            entities = session.query(clazz).all()
            return get_entities(array_name, entities, get_relation_entity_function)


@auth_required('get_by_id')
def get_entity_by_id(clazz, entity_id, array_name, get_relation_entity_function=None):
    entity_name = clazz.__name__
    if entity_name in SENSITIVE_DATA_CLASSES:
        return get_sensitive_data(array_name, get_relation_entity_function)
    else:
        with session_scope() as session:
            entities = session.query(clazz).filter_by(id=uuid.UUID(entity_id)).all()
            return get_entities(array_name, entities, get_relation_entity_function)


@auth_required('get_by_id')
def get_all_by_ids(clazz, ids, array_name, get_relation_entity_function=None):
    entity_name = clazz.__name__
    if entity_name in SENSITIVE_DATA_CLASSES:
        return get_sensitive_data_by_ids(ids, array_name, get_relation_entity_function)
    else:
        with session_scope() as session:
            entities = session.query(clazz).filter(clazz.id.in_(ids)).all()
            return get_entities(array_name, entities, get_relation_entity_function)