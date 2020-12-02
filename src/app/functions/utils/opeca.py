import pydoc

from app.constants import *
from app.functions.base.uuid import generate_uuid


def generate_order_number():
    return generate_uuid().replace('-', '')


def get_person_by_session_token(session, token):
    session_clazz = pydoc.locate(USER_SESSION_CLASS)
    user_session = session.query(session_clazz).filter_by(token=token).first()
    return user_session.person_id if user_session is not None else None


def get_user_session_by_token(session, token):
    session_clazz = pydoc.locate(USER_SESSION_CLASS)
    user_session = session.query(session_clazz).filter_by(token=token).first()
    return user_session