from app import engine


def row_count(query, **kwargs):
    connection = engine.connect()
    try:
        proxy = connection.execute(query, kwargs)
        rowcount = proxy.rowcount
        proxy.close()
        return rowcount
    finally:
        connection_close(connection)


def connection_close(connection):
    connection.close()


def first(query, **kwargs):
    connection = engine.connect()
    try:
        proxy = connection.execute(query, kwargs)
        first_row = proxy.first()
        proxy.close()
        return first_row
    finally:
        connection_close(connection)


def execute(query, **kwargs):
    connection = engine.connect()
    transaction = connection.begin()
    try:
        proxy = connection.execute(query, kwargs)
        transaction.commit()
        return proxy
    except:
        transaction.rollback()
        raise
    finally:
        connection_close(connection)


def select(query, **kwargs):
    connection = engine.connect()
    try:
        proxy = connection.execute(query, kwargs)
        return proxy
    finally:
        connection_close(connection)