from connexion.exceptions import ProblemException
from sqlalchemy.exc import InvalidRequestError, OperationalError, IntegrityError
from werkzeug.exceptions import HTTPException, BadRequest, Unauthorized

from app.classes.handling.storage import StorageBadRequest
from app.constants import RESOURCE_NOT_FOUND, PERMISSION_DENIED
from app.functions import app
from app.functions.handling.error_codes import *
from app.functions.io.response import fault
from app.functions.logging.logger import error, exception


@app.errorhandler(OperationalError)
def internal_database_error(error_instance):
    error("internal_database_error")
    exception(error_instance)
    message = str(error_instance)
    code = 500
    if isinstance(error_instance, HTTPException):
        code = error_instance.code
    title = 'Internal database error'
    return fault(message, STORAGE_0001, code, title)


@app.errorhandler(500)
def internal_server_error(error_instance):
    error("internal_server_error")
    exception(error_instance)
    message = str(error_instance)
    code = 500
    if isinstance(error_instance, HTTPException):
        code = error_instance.code
    title = 'Internal server error'
    return fault(message, STORAGE_0001, code, title)


@app.errorhandler(Exception)
def unhandled_exception(exception_instance):
    error("unhandled_exception")
    exception(exception_instance)
    message = str(exception_instance)
    return fault(message, STORAGE_0002, 404, RESOURCE_NOT_FOUND)


@app.errorhandler(BadRequest)
def bad_request(exception_instance):
    error("bad_request")
    exception(exception_instance)
    message = exception_instance.description
    code = 400
    title = 'Bad request'
    return fault(message, STORAGE_0004, code, title)


@app.errorhandler(ProblemException)
def connexion_bad_request(exception_instance):
    error("connexion_bad_request")
    exception(exception_instance)
    message = exception_instance.detail
    code = exception_instance.status
    title = exception_instance.title
    return fault(message, STORAGE_9999, code, title)


@app.errorhandler(Unauthorized)
def handle_forbidden(exception_instance):
    error("handle_forbidden")
    message = exception_instance.description
    return fault(message, STORAGE_0009, 403, PERMISSION_DENIED)


@app.errorhandler(NameError)
def name_error(error_instance):
    error("name_error")
    exception(error_instance)
    message = str(error_instance)
    code = 400
    title = 'Bad request'
    return fault(message, STORAGE_0010, code, title)


@app.errorhandler(ValueError)
def value_error(error_instance):
    error("value_error")
    exception(error_instance)
    message = str(error_instance)
    code = 400
    title = 'Bad request'
    return fault(message, STORAGE_0011, code, title)


@app.errorhandler(TypeError)
def type_error(error_instance):
    error("type_error")
    exception(error_instance)
    message = str(error_instance).replace("__init__() ", "")
    code = 400
    title = 'Bad request'
    return fault(message, STORAGE_0012, code, title)


@app.errorhandler(InvalidRequestError)
def invalid_request_error(error_instance):
    error("invalid_request_error")
    exception(error_instance)
    message = str(error_instance) \
        .replace("'", "") \
        .replace("class ", "") \
        .replace("app.classes.", "") \
        .replace("<", "") \
        .replace(">", "")
    code = 400
    title = 'Bad request'
    return fault(message, STORAGE_0013, code, title)


@app.errorhandler(IntegrityError)
def integrity_error(error_instance):
    error("integrity_error")
    exception(error_instance)
    if "unique constraint" in str(error_instance):
        message = "Unique constraint: please check request values on uniquiness"
    else:
        message = str(error_instance)
    code = 400
    title = 'Bad request'
    return fault(message, STORAGE_0014, code, title)


@app.errorhandler(StorageBadRequest)
def storage_bad_request(exception_instance):
    error("storage_bad_request")
    exception(exception_instance)
    message = exception_instance.description
    code = 409
    title = 'Bad request'
    return fault(message, exception_instance.error_code, code, title)
