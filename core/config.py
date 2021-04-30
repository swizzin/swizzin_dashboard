import pwd

class Config:
    try:
        ADMIN_USER = pwd.getpwuid(1000).pw_name
    except:
        ADMIN_USER = None
    APPLICATION_ROOT = '/'
    FLASK_HTPASSWD_PATH = '/etc/htpasswd'
    FLASK_SECRET = "What's the password?"
    FLASK_AUTH_REALM = "What's the password?"
    HOST = "0.0.0.0"
    PORT = "8333"
    RATELIMIT_ENABLED = True
    RATELIMIT_DEFAULT = "5 per minute"
    URLBASE = ""
    SHAREDSERVER = False
    FORMS_LOGIN = True
    NETWORK_TOTALS = False
