from app import app as swagger_app

app = swagger_app.app

REST_VERSION = app.config['REST_VERSION']
REST_GUIDE = app.config['REST_GUIDE']
APP_NAME = app.config['APP_NAME']

UPLOAD_DIRECTORY = app.config['UPLOAD_DIRECTORY']
UPLOAD_ABS_DIRECTORY = app.config['UPLOAD_ABS_DIRECTORY']
MEDIA_DIRECTORY = app.config['MEDIA_DIRECTORY']

ALLOWED_EXTENSIONS = app.config['ALLOWED_EXTENSIONS']

PROD_ENVIRONMENT = app.config['EXPECTED_GO_LIVE_ENV_NAME']
ENVIRONMENT = 'localhost'

isProdEnvironment = False
isDevEnvironment = True
isDebugRequestResponse = False
isDebugMode = app.config['DEBUG']

defaultDateFormat = app.config['DEFAULT_DATE_FORMAT']
defaultDateFormatMs = app.config['DEFAULT_DATE_FORMAT_MS']
defaultTimeZone = app.config['DEFAULT_TIME_ZONE']

from app.functions.handling.handler import *
