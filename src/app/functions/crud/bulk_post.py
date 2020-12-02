import uuid

from app.constants import IMPACTED_ENTITIES, ID, ENTITY_KEYS
from app.functions import REST_GUIDE
from app.functions.base.json import empty_json_object
from app.functions.base.uuid import generate_uuid
from app.functions.io.response import add_impacted_entity


def merge_entity(clazz, json, json_body, session, primary_key=ID, entity_db=None):
    entity_name = clazz.__name__
    action = ''
    key_field = ENTITY_KEYS[entity_name]
    key_value = ''
    try:
        if primary_key not in json:
            json[primary_key] = generate_uuid()
        if entity_db is None:
            entity_db = session.query(clazz).filter_by(id=uuid.UUID(json[primary_key]))
        # https://docs.sqlalchemy.org/en/13/orm/query.html?highlight=update#sqlalchemy.orm.query.Query.with_for_update
        entity_db = entity_db.with_for_update()
        entity_first = entity_db.first()
        if entity_first is None:
            action = 'insert'
            entity = clazz(**json)
            session.add(entity)
            key_value = entity.__getattribute__(key_field)
        else:
            action = 'update'
            entity_db.update(json)
            key_value = json.get(key_field)
    except:
        raise
    finally:
        entity_id = str(json[primary_key])
        if IMPACTED_ENTITIES not in json_body:
            json_body[IMPACTED_ENTITIES] = empty_json_object()
        json_body['type'] = REST_GUIDE + entity_name + 's'
        json_body['instance'] = \
            (json_body['instance'] if "instance" in json_body else '') + '/' + entity_name.lower() + '/' + entity_id
        json_body['action'] = action
        add_impacted_entity(key_value, entity_name, json_body)
