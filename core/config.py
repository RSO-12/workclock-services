import os

DB_URI = os.environ.get('DB_URI', 'localhost:8432')
DB_USER = os.environ.get('DB_USER', 'dbuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'postgres')
DB_NAME = os.environ.get('DB_NAME', 'workclock-db')
JWT_SECRET = os.environ.get('JWT_SECRET', 'default_value')