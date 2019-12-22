import os


class Config:
    SECRET_KEY = 'd5cb5e15d9dad92c5f284fd5b1cc6d98'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///good.db'
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASS')
