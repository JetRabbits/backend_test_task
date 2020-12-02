from werkzeug.exceptions import BadRequest

from app.functions.handling.error_codes import STORAGE_0100


class StorageBadRequest(BadRequest):
    error_code = STORAGE_0100

    def __init__(self, description=None, error_code=None):
        BadRequest.__init__(self)
        if description is not None:
            self.description = description
        if error_code is not None:
            self.error_code = error_code