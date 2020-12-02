from sqlalchemy import text

from app.functions import defaultTimeZone
from app.functions.utils.query import select


def get_employee_timezone(employee):
    query = '''select timezone from persons where id = uuid(:employee)'''
    employee_timezone_result = select(text(query), employee=employee)
    employee_timezone = employee_timezone_result.first()[
        'timezone'] if employee_timezone_result.rowcount > 0 else defaultTimeZone
    return employee_timezone