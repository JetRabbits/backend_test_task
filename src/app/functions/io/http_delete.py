import uuid

import requests
from werkzeug.exceptions import BadRequest

from app.constants import CLIENT_ROLE, SENSITIVE_DATA_CLASSES, RESOURCE_NOT_FOUND
from app.functions import REST_GUIDE
from app.functions.base.uuid import generate_uuid
from app.functions.handling.error_codes import STORAGE_0003
from app.functions.io.response import make_json_response, fault, success
from app.functions.utils.context import session_scope
from app.functions.utils.decorator import auth_required
from app.functions.utils.jwt import build_auth_headers


def get_private_token_url():
    raise BadRequest('not implemented')


def delete_private_response(private_url=None):
    private_url = private_url if private_url is not None else get_private_token_url()
    auth_headers = build_auth_headers({'id': generate_uuid()}, CLIENT_ROLE)
    response = requests.delete(private_url, headers=auth_headers)
    return response.json(), response.status_code


@auth_required('remove')
def delete_entity(clazz, entity_id, token):
    entity_name = clazz.__name__
    instance = '/' + entity_name.lower() + '/' + str(entity_id)
    if entity_name in SENSITIVE_DATA_CLASSES:
        json, code = delete_private_response()
        if code != 200:
            return make_json_response(json, code)

    with session_scope() as session:
        entity_db = session.query(clazz).filter_by(id=uuid.UUID(entity_id))
        if entity_db.first() is None:
            response = fault(entity_name + ' not found', STORAGE_0003, 404, RESOURCE_NOT_FOUND,
                             REST_GUIDE + entity_name + 's', instance, 'delete')
        else:
            entity_db.delete()
            response = success('DELETE /' + entity_name.lower() + '/' + entity_id, 200, 'Success',
                               REST_GUIDE + entity_name + 's', instance, 'delete')
    return response