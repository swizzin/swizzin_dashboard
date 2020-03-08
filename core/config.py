import pwd

class Config:
    ADMIN_USER = pwd.getpwuid(1000).pw_name
    APPLICATION_ROOT = '/'
    FLASK_HTPASSWD_PATH = '/etc/htpasswd'
    FLASK_SECRET = "What's the password?"
    HOST = "0.0.0.0"
    PORT = "8333"
    URL_BASE = "/"
    SHAREDSERVER = False
