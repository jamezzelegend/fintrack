from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from app.extensions import db
from app.forms import LoginForm, RegistrationForm
from app.models.user import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def index():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard.index'))
  return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard.index'))

  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(
      username=form.username.data.strip(),
      email=form.email.data.strip().lower(),
    )
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Account created successfully. Please sign in.', 'success')
    return redirect(url_for('auth.login'))

  return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('dashboard.index'))

  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data.strip()).first()
    if user and user.check_password(form.password.data):
      login_user(user, remember=True)
      next_page = request.args.get('next')
      if next_page and next_page.startswith('/'):
        return redirect(next_page)
      return redirect(url_for('dashboard.index'))
    flash('Invalid username or password.', 'danger')

  return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
  logout_user()
  flash('You have been logged out.', 'info')
  return redirect(url_for('auth.login'))
