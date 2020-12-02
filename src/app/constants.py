UNDEFINED = 'undefined'

GUEST_ROLE = -1
ADMIN_ROLE = 0
CURATOR_ROLE = 1
MANAGER_ROLE = 2
EMPLOYEE_ROLE = 3
CLIENT_ROLE = 4
RELATIVE_ROLE = 5
MAIN_RELATIVE_ROLE = 6

TOKEN_EXPIRATION_TIME = 86400

PERMISSION_DENIED = 'Permission denied'
RESOURCE_NOT_FOUND = 'Resource not found. Business logic error'

USER_SESSION_CLASS = 'app.classes.user_session.UserSession'

ALLOWED_STATUS_FOR_DETAILS = [400, 404]
INSTANCE = 'instance'
IMPACTED_ENTITIES = 'impacted_entities'
ATTACHMENT_DIRECTORY = 'attachments'
ID = str('id')

BYIDS_FILTER = 'byIds'
TYPE_PREFIX = '/rest/v1/ui/#/'
UTC_TIMEZONE = "+0000"

ENTITY_KEYS = {
    'UserSession': 'id',
    'Setting': 'key',
    'Node': 'id',
    'NodeReader': 'reader_id',
    'NodeWriter': 'writer_id'
}

SENSITIVE_DATA_CLASSES = []
SENSITIVE_DATA_EXCLUDED_FROM_MERGE_CLASSES = ['User']

DEFAULT_OWNER_ID = '00000000-0000-0000-0000-000000000000'
OWNER_ROLES = [ADMIN_ROLE, MANAGER_ROLE, EMPLOYEE_ROLE]

SERVER_DATA_PROVIDER = 'server'
SERVER_DATA_PROVIDER_ID = 1

FILE_PROVIDER_MAPPING = {
    SERVER_DATA_PROVIDER_ID: SERVER_DATA_PROVIDER,
}

GET_NODE_IDS_BY_PATH = '''select id from node_paths where path like :path'''