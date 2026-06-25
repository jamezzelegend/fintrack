from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import ProfileForm
from app.models.user import User

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')


@profile_bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
  form = ProfileForm(obj=current_user)

  if form.validate_on_submit():
    email = form.email.data.strip().lower()
    existing = User.query.filter(User.email == email, User.id != current_user.id).first()
    if existing:
      flash('Email is already registered.', 'danger')
      return render_template('profile/index.html', form=form)

    if form.new_password.data:
      if not form.current_password.data or not current_user.check_password(form.current_password.data):
        flash('Current password is incorrect.', 'danger')
        return render_template('profile/index.html', form=form)

      current_user.set_password(form.new_password.data)

    current_user.email = email
    db.session.commit()
    flash('Profile updated successfully.', 'success')
    return redirect(url_for('profile.index'))

  return render_template('profile/index.html', form=form)
