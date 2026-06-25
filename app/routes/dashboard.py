from flask import Blueprint, jsonify, render_template
from flask_login import current_user, login_required

from app.models.budget import Budget
from app.services import category_spending_current_month, expense_by_category, financial_summary, monthly_totals

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
  summary = financial_summary(current_user.id)
  budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.category).all()
  budget_data = []

  for budget in budgets:
    spent = category_spending_current_month(current_user.id, budget.category)
    percentage = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
    budget_data.append({
      'budget': budget,
      'spent': spent,
      'percentage': min(percentage, 100),
      'raw_percentage': percentage,
      'over_budget': spent > budget.monthly_limit,
    })

  return render_template('dashboard/index.html', summary=summary, budget_data=budget_data)


@dashboard_bp.route('/api/dashboard/charts')
@login_required
def chart_data():
  category_data = expense_by_category(current_user.id)
  monthly_data = monthly_totals(current_user.id, 12)

  return jsonify({
    'expense_breakdown': {
      'labels': list(category_data.keys()),
      'values': list(category_data.values()),
    },
    'monthly_trend': {
      'labels': [m['label'] for m in monthly_data],
      'income': [m['income'] for m in monthly_data],
      'expenses': [m['expenses'] for m in monthly_data],
    },
    'income_vs_expense': {
      'labels': [m['label'] for m in monthly_data],
      'income': [m['income'] for m in monthly_data],
      'expenses': [m['expenses'] for m in monthly_data],
    },
  })
