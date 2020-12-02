import json

from app.functions.base.encoder import AlchemyEncoder


def to_json_array(entities):
    json_array = json.loads('[]')
    for entity in entities:
        json_array.append(json.loads(json.dumps(entity, cls=AlchemyEncoder)))
    return json_array


def to_json(entity):
    return json.loads(json.dumps(entity, cls=AlchemyEncoder))


def json_to_string(response):
    return json.dumps(response, ensure_ascii=False, default=str)


def empty_json_array(array_name=None):
    return json.loads('{ "' + array_name + '": [] }') if array_name is not None else json.loads('[]')


def empty_json_object():
    return json.loads('{}')