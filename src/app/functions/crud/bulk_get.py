import uuid

from app.constants import BYIDS_FILTER
from app.functions.base.json import to_json, to_json_array, empty_json_array, empty_json_object
from app.functions.io.http_post import post_private_response
from app.functions.io.request import extract_private_token
from app.functions.io.response import make_json_response
from app.functions.utils.context import session_scope


def get_first_entity_by_id(clazz, id, session=None):
    if session is None:
        with session_scope() as session:
            return _get_first_entity_by_id(clazz, id, session)
    else:
        return _get_first_entity_by_id(clazz, id, session)


def _get_first_entity_by_id(clazz, id, session):
    entity = session.query(clazz).filter_by(id=uuid.UUID(id)).first()
    return to_json(entity)


def get_entities(array_name, entities, get_relation_entity_function=None):
    json_entities = empty_json_array(array_name)
    json_entities[array_name] = to_json_array(entities)
    if get_relation_entity_function is not None:
        json_array = json_entities[array_name]
        get_relation_entity_function(json_array)
    return make_json_response(json_entities, 200)


def get_sensitive_data_by_ids(ids, array_name, get_relation_entity_function):
    request = empty_json_object()
    request[BYIDS_FILTER] = ids
    request['token'] = extract_private_token()
    json, code = post_private_response(request)
    if code == 200 and get_relation_entity_function is not None:
        json_array = json[array_name]
        get_relation_entity_function(json_array)
    return make_json_response(json, code)