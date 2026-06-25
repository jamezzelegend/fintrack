from datetime import datetime, timezone

from app.extensions import db


class Budget(db.Model):
  __tablename__ = 'budgets'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
  category = db.Column(db.String(50), nullable=False)
  monthly_limit = db.Column(db.Float, nullable=False)
  created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

  __table_args__ = (
    db.UniqueConstraint('user_id', 'category', name='uq_user_category_budget'),
    db.CheckConstraint('monthly_limit > 0', name='check_monthly_limit_positive'),
  )

  def __repr__(self):
    return f'<Budget {self.category} {self.monthly_limit}>'
