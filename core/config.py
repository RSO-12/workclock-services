import os

# db config
DB_URI = os.environ.get('DB_URI', 'localhost:8432')
DB_USER = os.environ.get('DB_USER', 'dbuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'workclock-db')

# jwt secret
JWT_SECRET = os.environ.get('JWT_SECRET', 'default_value')

# mailer config
SMTP_SENDER = os.environ.get('SMTP_SENDER', '')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')

# is dev
IS_DEV = os.environ.get('IS_DEV', False)