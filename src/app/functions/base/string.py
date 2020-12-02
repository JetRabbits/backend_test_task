import re


def replace(string, pattern, sub):
    return re.sub('%s$' % pattern, sub, string)


def check_string_on_null(value):
    if value is None:
        value = ''
    return value
