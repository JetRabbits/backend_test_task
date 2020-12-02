import os

basedir = os.path.abspath(os.path.dirname(__file__))

# FLASK
STORAGE_AUTH_SALT = 'QK4-?u02&S8pslx-u  #~r]Q?p`]a*w+4 +|F6xc&!/T4z06d8zLg[+-tSLE,vDt'
APP_NAME = os.environ.get("APP_NAME") or "localhost"
SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(24)
WTF_CSRF_ENABLED = True
JSON_AS_ASCII = False
DEBUG = (os.environ.get("DEBUG_MODE") == 'True') or False
SQLALCHEMY_ECHO = DEBUG
SQLALCHEMY_RECORD_QUERIES = DEBUG

# STORAGE
DEFAULT_TIME_ZONE = '+0300'
DEFAULT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%S%z'
DEFAULT_DATE_FORMAT_MS = '%Y-%m-%dT%H:%M:%S.%f%z'

# REST
REST_VERSION = '0.1'
REST_GUIDE = '/rest/v1/ui/#/'

# Environment settings
EXPECTED_GO_LIVE_ENV_NAME = 'prod'
DEBUG_REQUEST_RESPONSE = False
UPLOAD_DIRECTORY = "files"
UPLOAD_ABS_DIRECTORY = "/opt/services/flaskapp/src/files"
MEDIA_DIRECTORY = "media"
ALLOWED_EXTENSIONS = {'json', 'png', 'jpg', 'jpeg', 'gif', 'txt'}
MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH")) or 1048576

# Logstash
LOG_STASH_SERVER = '127.0.0.1'
LOG_STASH_PORT = 5000