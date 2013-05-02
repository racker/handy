from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read('etc/handy.conf')

AUTH_FLAG = parser.get('auth', 'auth_on').lower()
if AUTH_FLAG == "true":
     AUTH_URL = parser.get('auth', 'url')
     USERNAME = parser.get('auth', 'username')
     PASSWORD = parser.get('auth', 'password')

BASE_SERVER = parser.get("marconi_env", "marconi_url")
MARCONI_VERSION = parser.get("marconi_env", "marconi_version")
TENANT_ID = parser.get("marconi_env", "tenant_id")

BASE_URL = BASE_SERVER + "/" + MARCONI_VERSION + "/" + TENANT_ID

HOST = parser.get("header_values", "host")
USER_AGENT = parser.get("header_values", "useragent")
