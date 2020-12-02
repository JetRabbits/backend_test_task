import datetime
import json
import uuid

from sqlalchemy.ext.declarative import DeclarativeMeta

from app.functions.base.date import convert_date_to_string


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                if isinstance(data, datetime.datetime):
                    date = convert_date_to_string(data)
                    json.dumps(date)
                    fields[field] = date
                elif isinstance(data, uuid.UUID):
                    uuid_id = data.__str__()
                    json.dumps(uuid_id)
                    fields[field] = uuid_id
                else:
                    json.dumps(data)
                    fields[field] = data
            return fields

        return json.JSONEncoder.default(self, obj)