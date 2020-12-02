import os

import connexion
# noinspection PyUnresolvedReferences
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = os.environ['POSTGRES_HOST']
port = os.environ['POSTGRES_PORT']
db = os.environ['POSTGRES_DB']
user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
MAX_OVERFLOW = int(os.environ['MAX_OVERFLOW'])
POOL_SIZE = int(os.environ['POOL_SIZE'])
POOL_RECYCLE = int(os.environ['POOL_RECYCLE'])
POOL_TIMEOUT = int(os.environ['POOL_TIMEOUT'])

# https://docs.sqlalchemy.org/en/13/core/engines.html
connection = (user, pwd, host, port, db)
engine = create_engine('postgres://%s:%s@%s:%s/%s' % connection, max_overflow=MAX_OVERFLOW,
                       pool_size=POOL_SIZE, pool_recycle=POOL_RECYCLE, pool_timeout=POOL_TIMEOUT)
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)

app = connexion.App(__name__, specification_dir='./v1')
app.app.config.from_object('config')
app.add_api('swagger.yml')

toolbar = DebugToolbarExtension(app.app)
app.app.config['DEBUG_TB_PANELS'] += ('flask_debugtoolbar_sqlalchemy.SQLAlchemyPanel',)
app.app.extensions = getattr(app.app, 'extensions', {})
app.app.extensions['debugtoolbar'] = toolbar

from app.functions.logging.logger import init_loggers

init_loggers()
