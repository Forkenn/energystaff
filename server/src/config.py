import os

DEBUG = int(os.environ.get('DEBUG'))

DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')

SECRET_TOKEN = os.environ.get('SECRET_TOKEN')
TOKEN_EXPIRE_MINUTES = 10000
COOKIE_NAME = "energystaff_token"
