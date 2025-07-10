from typing import Union


class DefaultConfig:
    DEVELOPMENT = False
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY: Union[bytes, str] = "this-really-needs-to-be-changed"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DB_NAME = "pypi.sqlite3"
    DEPLOY_PREFIX = ""


class ProductionConfig(DefaultConfig):
    DEPLOY_PREFIX = "/pypi"
    SECRET_KEY = b'_5#xU7"F4Q8z\n\xec]/'


class DevelopmentConfig(DefaultConfig):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(DefaultConfig):
    TESTING = True
    SECRET_KEY = "test"
    DB_NAME = "pypi_test.sqlite3"
    WTF_CSRF_ENABLED = False
