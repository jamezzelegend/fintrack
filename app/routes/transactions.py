from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import TransactionForm
from app.models.transaction import CATEGORIES, Transaction
from config import Config

transactions_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

SORT_COLUMNS = {
  'date': Transaction.transaction_date,
  'amount': Transaction.amount,
  'category': Transaction.category,
  'type': Transaction.transaction_type,
  'created': Transaction.created_at,
}


@transactions_bp.route('/')
@login_required
def list_transactions():
  page = request.args.get('page', 1, type=int)
  search = request.args.get('q', '', type=str).strip()
  category = request.args.get('category', '', type=str).strip()
  date_from = request.args.get('date_from', '', type=str).strip()
  date_to = request.args.get('date_to', '', type=str).strip()
  sort = request.args.get('sort', 'date', type=str)
  order = request.args.get('order', 'desc', type=str)

  query = Transaction.query.filter_by(user_id=current_user.id)

  if search:
    query = query.filter(Transaction.description.ilike(f'%{search}%'))
  if category and category in CATEGORIES:
    query = query.filter(Transaction.category == category)
  if date_from:
    try:
      parsed_from = datetime.strptime(date_from, '%Y-%m-%d').date()
      query = query.filter(Transaction.transaction_date >= parsed_from)
    except ValueError:
      flash('Invalid start date format. Use YYYY-MM-DD.', 'warning')
  if date_to:
    try:
      parsed_to = datetime.strptime(date_to, '%Y-%m-%d').date()
      query = query.filter(Transaction.transaction_date <= parsed_to)
    except ValueError:
      flash('Invalid end date format. Use YYYY-MM-DD.', 'warning')

  sort_column = SORT_COLUMNS.get(sort, Transaction.transaction_date)
  if order == 'asc':
    query = query.order_by(sort_column.asc())
  else:
    query = query.order_by(sort_column.desc())

  pagination = query.paginate(
    page=page,
    per_page=Config.TRANSACTIONS_PER_PAGE,
    error_out=False,
  )

  return render_template(
    'transactions/list.html',
    transactions=pagination.items,
    pagination=pagination,
    categories=CATEGORIES,
    filters={
      'q': search,
      'category': category,
      'date_from': date_from,
      'date_to': date_to,
      'sort': sort,
      'order': order,
    },
  )


@transactions_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  form = TransactionForm()
  if request.method == 'GET':
    form.transaction_date.data = date.today()

  if form.validate_on_submit():
    transaction = Transaction(
      user_id=current_user.id,
      amount=round(form.amount.data, 2),
      category=form.category.data,
      description=form.description.data.strip(),
      transaction_type=form.transaction_type.data,
      transaction_date=form.transaction_date.data,
    )
    db.session.add(transaction)
    db.session.commit()
    flash('Transaction created successfully.', 'success')
    return redirect(url_for('transactions.list_transactions'))

  return render_template('transactions/form.html', form=form, title='Add Transaction')


@transactions_bp.route('/<int:transaction_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(transaction_id):
  transaction = Transaction.query.filter_by(
    id=transaction_id,
    user_id=current_user.id,
  ).first_or_404()

  form = TransactionForm(obj=transaction)
  if form.validate_on_submit():
    transaction.amount = round(form.amount.data, 2)
    transaction.category = form.category.data
    transaction.description = form.description.data.strip()
    transaction.transaction_type = form.transaction_type.data
    transaction.transaction_date = form.transaction_date.data
    db.session.commit()
    flash('Transaction updated successfully.', 'success')
    return redirect(url_for('transactions.list_transactions'))

  return render_template('transactions/form.html', form=form, title='Edit Transaction', transaction=transaction)


@transactions_bp.route('/<int:transaction_id>/delete', methods=['POST'])
@login_required
def delete(transaction_id):
  transaction = Transaction.query.filter_by(
    id=transaction_id,
    user_id=current_user.id,
  ).first_or_404()

  db.session.delete(transaction)
  db.session.commit()
  flash('Transaction deleted.', 'info')
  return redirect(url_for('transactions.list_transactions'))
