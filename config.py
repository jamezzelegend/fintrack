import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

_db_url = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'database', 'fintrack.db'))
if _db_url.startswith('postgres://'):
  _db_url = _db_url.replace('postgres://', 'postgresql://', 1)


class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY', 'Jameszhang)2')
  SQLALCHEMY_DATABASE_URI = _db_url
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  PERMANENT_SESSION_LIFETIME = timedelta(days=7)
  WTF_CSRF_ENABLED = True
  TRANSACTIONS_PER_PAGE = 15
