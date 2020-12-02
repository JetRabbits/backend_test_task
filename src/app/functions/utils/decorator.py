from app.constants import PERMISSION_DENIED
from app.functions.handling.error_codes import STORAGE_0000
from app.functions.io.request import request_parameters, get_ip, security_path
from app.functions.io.response import fault
from app.functions.utils.jwt import verify_auth_token


def auth_required(operation, path=None):
    def decorator(func):
        def func_wrapper(*args, **kwargs):
            verified = verify_auth_token(request_parameters().get('token'), get_ip(), security_path(path), operation)
            if not verified:
                response = fault(PERMISSION_DENIED, STORAGE_0000, 419, PERMISSION_DENIED)
            else:
                response = func(*args, **kwargs)
            return response
        return func_wrapper
    return decorator
