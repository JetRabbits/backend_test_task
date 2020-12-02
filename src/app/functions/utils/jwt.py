import os
import time

import jwt
from flask import request, g, jsonify
from werkzeug.exceptions import Unauthorized

from app.constants import CLIENT_ROLE, TOKEN_EXPIRATION_TIME
from app.functions import app
from app.functions.logging.logger import error, info, exception
from app.functions.utils.query import first

SECRET_KEY2 = "Not implemented yet"


def extract_token():
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise Unauthorized

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        return jsonify({'error': 'Authorization header must start with Bearer'}), 403, {
            'Content-Type': 'application/json; charset=utf-8'}
    elif len(parts) == 1:
        return Unauthorized('Token not found')
    elif len(parts) > 2:
        return jsonify({'error': 'Authorization header must be "Bearer token"'}), 403, {
            'Content-Type': 'application/json; charset=utf-8'}

    token = parts[1]
    return token


def decode_token(token):
    return decode_jwt_token(token, app.config['SECRET_KEY'])


def decode_jwt_token(token, secret):
    try:
        decode = jwt.decode(token, secret, algorithms=['HS256'])
        return decode
    except jwt.ExpiredSignatureError:
        error('Permission denied. Token expired')
        raise Unauthorized('Permission denied. Token expired')
    except jwt.DecodeError:
        error('Permission denied. Wrong token')
        raise Unauthorized('Permission denied. Wrong token')


def encode_token(value_for_encode):
    token = encode_jwt_token(value_for_encode, app.config['SECRET_KEY'], CLIENT_ROLE)
    if "token" not in g:
        g.token = token
    return token


def encode_jwt_token(payload, secret, role_id=None):
    payload['exp'] = int(time.time()) + TOKEN_EXPIRATION_TIME
    if role_id is not None:
        payload['role_id'] = role_id
    token = jwt.encode(payload, secret, algorithm='HS256').decode('utf-8')
    return token


def build_auth_headers(value_for_encode, role_id=None):
    jwt_token = encode_jwt_token(value_for_encode, SECRET_KEY2, role_id)
    return {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + jwt_token}


# TODO-2: Refactor to simplify code
def verify_auth_token(token, ip='0.0.0.0', path='/', grant='get_all', raise_error=True):
    token_checked = ("token_checked" in g and g.token_checked)
    if token_checked:
        return True

    if '127.0.0.1' in ip or '0.0.0.0' in ip:
        info('Permission granted. System request.')
        g.token_checked = True
        return True

    try:
        payload = decode_token(token)
        if "login" in payload:
            g.login = payload['login']
        if "id" in payload:
            g.user_id = payload['id']
        if "role" in payload:
            g.user_role = payload['role']
    except Exception as e:
        exception(e)
        if raise_error:
            raise e
        else:
            return False

    permission = check_grants(payload['role'], path, grant)
    if permission is None:
        error('Permission denied. No rights for ' + path)
        if raise_error:
            raise Unauthorized('Permission denied. No rights for ' + path)
        else:
            return False

    g.token_checked = True
    return True


def check_grants(role, url, grant):
    query = \
        'select 1 from grants g where g.role = ' + str(role) + ' and g.url = \'' + url + '\' and ' + grant + ' = true'
    return first(query)
