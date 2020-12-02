# coding=utf-8
from app.functions.utils.rest import get_health, get_version


def version():
    return get_version()


def health():
    return get_health()
