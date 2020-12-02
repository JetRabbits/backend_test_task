import uuid

from app.constants import ID


def generate_uuid():
    return uuid.uuid1().__str__()


def specify_id(json, array_name):
    if array_name in json:
        for json in json[array_name]:
            if "id" not in json:
                json[ID] = generate_uuid()