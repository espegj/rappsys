
class BaseConfig(object):
    SECRET_KEY = 'super-secret'
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 13
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost:3306/flask_test'
    SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
    # Replace this with your own salt.
    SECURITY_PASSWORD_SALT = 'xxxxxxxxxxxxxxx'
    SECURITY_REGISTERABLE = True

    # Flask-Security optionally sends email notification to users upon registration, password reset, etc.
    # It uses Flask-Mail behind the scenes.
    # Set mail-related config values.
    # Replace this with your own "from" address
    SECURITY_EMAIL_SENDER = 'webcoreconsulting@gmail.com'
    # Replace the next five lines with your own SMTP server settings
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'webcoreconsulting@gmail.com'
    MAIL_PASSWORD = 'QA5-as3-MVU-5LW'
    SECURITY_MSG_EMAIL_ALREADY_ASSOCIATED = ('Mailen er allerede registrert', 'error')
    SECURITY_MSG_INVALID_PASSWORD = ('Feil passord', 'error')
    SECURITY_MSG_USER_DOES_NOT_EXIST = ('Bruker finnes ikke', 'error')
