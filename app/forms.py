from flask_wtf import FlaskForm
from wtforms import DateField, FloatField, PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional, ValidationError

from app.models.transaction import CATEGORIES, TRANSACTION_TYPES
from app.models.user import User


class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[
    DataRequired(),
    Length(min=3, max=80),
  ])
  email = StringField('Email', validators=[
    DataRequired(),
    Email(),
    Length(max=120),
  ])
  password = PasswordField('Password', validators=[
    DataRequired(),
    Length(min=8, max=128),
  ])
  confirm_password = PasswordField('Confirm Password', validators=[
    DataRequired(),
    EqualTo('password', message='Passwords must match.'),
  ])
  submit = SubmitField('Create Account')

  def validate_username(self, field):
    if User.query.filter_by(username=field.data.strip()).first():
      raise ValidationError('Username is already taken.')

  def validate_email(self, field):
    if User.query.filter_by(email=field.data.strip().lower()).first():
      raise ValidationError('Email is already registered.')


class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired(), Length(max=80)])
  password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign In')


class TransactionForm(FlaskForm):
  amount = FloatField('Amount', validators=[
    DataRequired(),
    NumberRange(min=0.01, message='Amount must be greater than zero.'),
  ])
  category = SelectField('Category', choices=[(c, c) for c in CATEGORIES], validators=[DataRequired()])
  description = StringField('Description', validators=[DataRequired(), Length(max=255)])
  transaction_type = SelectField(
    'Type',
    choices=[(t, t) for t in TRANSACTION_TYPES],
    validators=[DataRequired()],
  )
  transaction_date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
  submit = SubmitField('Save Transaction')


class BudgetForm(FlaskForm):
  category = SelectField('Category', choices=[], validators=[DataRequired()])
  monthly_limit = FloatField('Monthly Limit', validators=[
    DataRequired(),
    NumberRange(min=0.01, message='Limit must be greater than zero.'),
  ])
  submit = SubmitField('Save Budget')


class ProfileForm(FlaskForm):
  email = StringField('Email', validators=[
    DataRequired(),
    Email(),
    Length(max=120),
  ])
  current_password = PasswordField('Current Password')
  new_password = PasswordField('New Password', validators=[
    Optional(),
    Length(min=8, max=128),
  ])
  confirm_password = PasswordField('Confirm New Password', validators=[
    EqualTo('new_password', message='Passwords must match.'),
  ])
  submit = SubmitField('Update Profile')
