from flask import Blueprint, jsonify, render_template
from flask_login import current_user, login_required

from app.models.budget import Budget
from app.services import analytics_stats, category_spending_current_month, expense_by_category, monthly_totals

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')


@analytics_bp.route('/')
@login_required
def index():
  stats = analytics_stats(current_user.id)
  return render_template('analytics/index.html', stats=stats)


@analytics_bp.route('/api/charts')
@login_required
def chart_data():
  stats = analytics_stats(current_user.id)
  category_totals = stats['category_totals']
  monthly_data = stats['monthly_data']

  budgets = Budget.query.filter_by(user_id=current_user.id).all()
  budget_utilization = []
  for budget in budgets:
    spent = category_spending_current_month(current_user.id, budget.category)
    utilization = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
    budget_utilization.append({
      'category': budget.category,
      'spent': spent,
      'limit': budget.monthly_limit,
      'utilization': round(utilization, 1),
    })

  ranked_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)

  return jsonify({
    'category_rankings': {
      'labels': [c[0] for c in ranked_categories],
      'values': [c[1] for c in ranked_categories],
    },
    'monthly_trend': {
      'labels': [m['label'] for m in monthly_data],
      'income': [m['income'] for m in monthly_data],
      'expenses': [m['expenses'] for m in monthly_data],
      'net': [m['net'] for m in monthly_data],
    },
    'budget_utilization': {
      'labels': [b['category'] for b in budget_utilization],
      'spent': [b['spent'] for b in budget_utilization],
      'limits': [b['limit'] for b in budget_utilization],
      'utilization': [b['utilization'] for b in budget_utilization],
    },
  })
