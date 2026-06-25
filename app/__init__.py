import os

from flask import Flask

from app.extensions import csrf, db, login_manager
from config import Config


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  os.makedirs(os.path.join(app.root_path, '..', 'database'), exist_ok=True)

  db.init_app(app)
  login_manager.init_app(app)
  csrf.init_app(app)

  from app.models.user import User

  @login_manager.user_loader
  def load_user(user_id):
    return db.session.get(User, int(user_id))

  from app.routes.auth import auth_bp
  from app.routes.dashboard import dashboard_bp
  from app.routes.transactions import transactions_bp
  from app.routes.budgets import budgets_bp
  from app.routes.analytics import analytics_bp
  from app.routes.profile import profile_bp

  app.register_blueprint(auth_bp)
  app.register_blueprint(dashboard_bp)
  app.register_blueprint(transactions_bp)
  app.register_blueprint(budgets_bp)
  app.register_blueprint(analytics_bp)
  app.register_blueprint(profile_bp)

  with app.app_context():
    db.create_all()

  @app.template_filter('currency')
  def currency_filter(value):
    return f'${value:,.2f}'

  @app.template_filter('percent')
  def percent_filter(value):
    return f'{value:.1f}%'

  return app
