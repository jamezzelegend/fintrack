import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY', 'fintrack-dev-secret-change-in-production')
  SQLALCHEMY_DATABASE_URI = os.environ.get(
    'DATABASE_URL',
    'sqlite:///' + os.path.join(BASE_DIR, 'database', 'fintrack.db')
  )
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  PERMANENT_SESSION_LIFETIME = timedelta(days=7)
  WTF_CSRF_ENABLED = True
  TRANSACTIONS_PER_PAGE = 15
