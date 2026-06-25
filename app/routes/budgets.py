from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app.extensions import db
from app.forms import BudgetForm
from app.models.budget import Budget
from app.models.transaction import EXPENSE_CATEGORIES
from app.services import category_spending_current_month

budgets_bp = Blueprint('budgets', __name__, url_prefix='/budgets')


def _budget_form_with_categories(exclude_category=None):
  existing = {
    b.category for b in Budget.query.filter_by(user_id=current_user.id).all()
  }
  if exclude_category:
    existing.discard(exclude_category)

  available = [c for c in EXPENSE_CATEGORIES if c not in existing]
  form = BudgetForm()
  form.category.choices = [(c, c) for c in available]
  return form


@budgets_bp.route('/')
@login_required
def list_budgets():
  budgets = Budget.query.filter_by(user_id=current_user.id).order_by(Budget.category).all()
  budget_data = []

  for budget in budgets:
    spent = category_spending_current_month(current_user.id, budget.category)
    percentage = (spent / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0
    budget_data.append({
      'budget': budget,
      'spent': spent,
      'remaining': max(budget.monthly_limit - spent, 0),
      'percentage': min(percentage, 100),
      'raw_percentage': percentage,
      'over_budget': spent > budget.monthly_limit,
    })

  return render_template('budgets/list.html', budget_data=budget_data)


@budgets_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  form = _budget_form_with_categories()
  if not form.category.choices:
    flash('Budgets already exist for all expense categories.', 'info')
    return redirect(url_for('budgets.list_budgets'))

  if form.validate_on_submit():
    budget = Budget(
      user_id=current_user.id,
      category=form.category.data,
      monthly_limit=round(form.monthly_limit.data, 2),
    )
    db.session.add(budget)
    db.session.commit()
    flash('Budget created successfully.', 'success')
    return redirect(url_for('budgets.list_budgets'))

  return render_template('budgets/form.html', form=form, title='Create Budget')


@budgets_bp.route('/<int:budget_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(budget_id):
  budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first_or_404()
  form = _budget_form_with_categories(exclude_category=budget.category)

  if request.method == 'GET':
    form.category.data = budget.category
    form.monthly_limit.data = budget.monthly_limit
  elif form.validate_on_submit():
    budget.monthly_limit = round(form.monthly_limit.data, 2)
    db.session.commit()
    flash('Budget updated successfully.', 'success')
    return redirect(url_for('budgets.list_budgets'))

  form.category.choices = [(budget.category, budget.category)]
  return render_template('budgets/form.html', form=form, title='Edit Budget', budget=budget)


@budgets_bp.route('/<int:budget_id>/delete', methods=['POST'])
@login_required
def delete(budget_id):
  budget = Budget.query.filter_by(id=budget_id, user_id=current_user.id).first_or_404()
  db.session.delete(budget)
  db.session.commit()
  flash('Budget deleted.', 'info')
  return redirect(url_for('budgets.list_budgets'))
