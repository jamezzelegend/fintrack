from datetime import datetime, timezone

from app.extensions import db

TRANSACTION_TYPES = ('Income', 'Expense')

CATEGORIES = (
  'Housing',
  'Food',
  'Transportation',
  'Entertainment',
  'Healthcare',
  'Utilities',
  'Shopping',
  'Salary',
  'Investments',
  'Miscellaneous',
)

EXPENSE_CATEGORIES = [c for c in CATEGORIES if c not in ('Salary', 'Investments')]
INCOME_CATEGORIES = ['Salary', 'Investments', 'Miscellaneous']


class Transaction(db.Model):
  __tablename__ = 'transactions'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
  amount = db.Column(db.Float, nullable=False)
  category = db.Column(db.String(50), nullable=False, index=True)
  description = db.Column(db.String(255), nullable=False, default='')
  transaction_type = db.Column(db.String(10), nullable=False, index=True)
  transaction_date = db.Column(db.Date, nullable=False, index=True)
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

  __table_args__ = (
    db.CheckConstraint('amount > 0', name='check_amount_positive'),
    db.CheckConstraint(
      "transaction_type IN ('Income', 'Expense')",
      name='check_transaction_type',
    ),
  )

  def __repr__(self):
    return f'<Transaction {self.id} {self.transaction_type} {self.amount}>'
