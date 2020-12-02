import datetime
from datetime import timezone

from sqlalchemy import text

from app.functions import defaultDateFormat
from app.functions import defaultDateFormatMs
from app.functions.handling.error_codes import STORAGE_0900
from app.classes.handling.storage import StorageBadRequest
from app.functions.utils.query import first


def now():
    return datetime.datetime.now(timezone.utc)


def convert_date(content):
    input_datetime = datetime.datetime.strptime(content, defaultDateFormat)
    server_datetime = now()
    if abs(input_datetime.year - server_datetime.year) > 1:
        raise StorageBadRequest('wrong input date: ' + content, STORAGE_0900)
    return input_datetime


def convert_date_to_string(content):
    return content.strftime(defaultDateFormat)


def convert_date_with_ms_to_string(content):
    return content.strftime(defaultDateFormatMs)


def convert_to_utc_date(content):
    query = '''select to_char(TIMESTAMP WITH TIME ZONE :content, 'YYYY-MM-DD"T"HH24:MI:SSOF00') as utc_time from dual'''
    return first(text(query), content=content)['utc_time']


def get_date_before_now(days_before_now):
    query = '''select to_char(NOW() - INTERVAL '%s DAY', 'DD.MM.YYYY') as requested_date from dual'''
    return first(text(query % days_before_now))['requested_date']