from contextlib import contextmanager

from app import Session


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session_close(session)


def session_close(session):
    session.close()
