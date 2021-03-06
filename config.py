import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    FLASKY_MAIL_SUBJECT_PREFIX = '[Valureach Onboarding]'
    FLASKY_MAIL_SENDER = 'Valureach Onboarding <do-not-reply>'
    FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    # mysql://username:password@server/db
    a = os.environ
    SQLALCHEMY_DATABASE_URI = "mysql://root:valuereachdb@localhost:3306/valuereach"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:valuereachdb@localhost:3306/valuereach"


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:valuereachdb@localhost:3306/valuereach"
 



config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': ProductionConfig
}
