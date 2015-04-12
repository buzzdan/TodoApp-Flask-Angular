# based on - https://realpython.com/blog/python/flask-by-example-part-1-project-setup/


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'this-really-needs-to-be-changed'
    DB_CONNECTION_STRING = 'mongodb://<dbuser>:<dbpassword>@ds061767.mongolab.com:61767/heroku_app35710471'

class ProductionConfig(Config):
    DEBUG = False
    DB_CONNECTION_STRING = 'somewhere in heroku :)'


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    DB_CONNECTION_STRING = 'mongodb://localhost/mydb'


class TestingConfig(Config):
    TESTING = True
