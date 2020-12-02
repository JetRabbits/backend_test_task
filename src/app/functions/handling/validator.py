import uuid

from werkzeug.exceptions import BadRequest

from app.constants import ID


def is_exist_by_id(clazz, entity_id, session):
    entity_name = clazz.__name__
    if session.query(clazz).filter_by(id=uuid.UUID(entity_id)).first() is None:
        raise BadRequest(entity_name + ' is not registered, id: ' + entity_id)


def check_required(key, json, array_name, entity_id=''):
    if key not in json:
        raise BadRequest("'" + key + "' is a required property - '" + array_name + "." + entity_id + "'")


def check_id(json, array_name):
    if ID not in json:
        raise BadRequest("'" + ID + "' is a required property - '" + array_name)