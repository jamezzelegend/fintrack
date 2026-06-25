from datetime import date
from calendar import monthrange

from sqlalchemy import func

from app.extensions import db
from app.models.transaction import Transaction


def get_month_bounds(year=None, month=None):
  today = date.today()
  year = year or today.year
  month = month or today.month
  start = date(year, month, 1)
  _, last_day = monthrange(year, month)
  end = date(year, month, last_day)
  return start, end


def sum_by_type(user_id, transaction_type, start=None, end=None):
  query = db.session.query(func.coalesce(func.sum(Transaction.amount), 0.0)).filter(
    Transaction.user_id == user_id,
    Transaction.transaction_type == transaction_type,
  )
  if start:
    query = query.filter(Transaction.transaction_date >= start)
  if end:
    query = query.filter(Transaction.transaction_date <= end)
  return float(query.scalar())


def expense_by_category(user_id, start=None, end=None):
  query = (
    db.session.query(Transaction.category, func.sum(Transaction.amount).label('total'))
    .filter(
      Transaction.user_id == user_id,
      Transaction.transaction_type == 'Expense',
    )
    .group_by(Transaction.category)
    .order_by(func.sum(Transaction.amount).desc())
  )
  if start:
    query = query.filter(Transaction.transaction_date >= start)
  if end:
    query = query.filter(Transaction.transaction_date <= end)
  return {row.category: float(row.total) for row in query.all()}


def monthly_totals(user_id, months=12):
  today = date.today()
  results = []

  for i in range(months - 1, -1, -1):
    month = today.month - i
    year = today.year
    while month <= 0:
      month += 12
      year -= 1

    start, end = get_month_bounds(year, month)
    income = sum_by_type(user_id, 'Income', start, end)
    expenses = sum_by_type(user_id, 'Expense', start, end)
    label = start.strftime('%b %Y')
    results.append({
      'label': label,
      'year': year,
      'month': month,
      'income': income,
      'expenses': expenses,
      'net': income - expenses,
    })

  return results


def category_spending_current_month(user_id, category):
  start, end = get_month_bounds()
  result = (
    db.session.query(func.coalesce(func.sum(Transaction.amount), 0.0))
    .filter(
      Transaction.user_id == user_id,
      Transaction.transaction_type == 'Expense',
      Transaction.category == category,
      Transaction.transaction_date >= start,
      Transaction.transaction_date <= end,
    )
    .scalar()
  )
  return float(result)


def financial_summary(user_id):
  total_income = sum_by_type(user_id, 'Income')
  total_expenses = sum_by_type(user_id, 'Expense')
  start, end = get_month_bounds()
  monthly_income = sum_by_type(user_id, 'Income', start, end)
  monthly_expenses = sum_by_type(user_id, 'Expense', start, end)

  return {
    'total_income': total_income,
    'total_expenses': total_expenses,
    'net_balance': total_income - total_expenses,
    'monthly_income': monthly_income,
    'monthly_expenses': monthly_expenses,
  }


def analytics_stats(user_id):
  summary = financial_summary(user_id)
  monthly_data = monthly_totals(user_id, 12)

  expense_months = [m['expenses'] for m in monthly_data if m['expenses'] > 0]
  income_months = [m['income'] for m in monthly_data if m['income'] > 0]

  avg_monthly_spending = sum(expense_months) / len(expense_months) if expense_months else 0.0
  avg_monthly_income = sum(income_months) / len(income_months) if income_months else 0.0

  savings_rate = 0.0
  if avg_monthly_income > 0:
    savings_rate = ((avg_monthly_income - avg_monthly_spending) / avg_monthly_income) * 100

  category_totals = expense_by_category(user_id)
  highest_category = max(category_totals, key=category_totals.get) if category_totals else None
  highest_category_amount = category_totals.get(highest_category, 0.0) if highest_category else 0.0

  largest_expense = (
    db.session.query(Transaction)
    .filter(Transaction.user_id == user_id, Transaction.transaction_type == 'Expense')
    .order_by(Transaction.amount.desc())
    .first()
  )

  return {
    **summary,
    'avg_monthly_spending': avg_monthly_spending,
    'avg_monthly_income': avg_monthly_income,
    'savings_rate': savings_rate,
    'highest_category': highest_category,
    'highest_category_amount': highest_category_amount,
    'largest_expense': largest_expense,
    'category_totals': category_totals,
    'monthly_data': monthly_data,
  }
