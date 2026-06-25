import random
from datetime import date, timedelta

from app import create_app
from app.extensions import db
from app.models.budget import Budget
from app.models.transaction import EXPENSE_CATEGORIES, Transaction
from app.models.user import User

EXPENSE_DETAILS = {
  'Housing': ['Monthly rent', 'Mortgage payment', 'Property tax', 'Home insurance', 'HOA fees'],
  'Food': ['Grocery shopping', 'Restaurant dinner', 'Coffee shop', 'Fast food', 'Farmers market'],
  'Transportation': ['Gas fill-up', 'Uber ride', 'Car insurance', 'Parking fee', 'Oil change'],
  'Entertainment': ['Movie tickets', 'Streaming subscription', 'Concert tickets', 'Video games', 'Bowling night'],
  'Healthcare': ['Doctor visit', 'Pharmacy prescription', 'Dental checkup', 'Gym membership', 'Vision exam'],
  'Utilities': ['Electric bill', 'Water bill', 'Internet service', 'Phone bill', 'Gas utility'],
  'Shopping': ['Clothing purchase', 'Electronics', 'Home supplies', 'Amazon order', 'Gift purchase'],
  'Miscellaneous': ['Bank fee', 'Donation', 'Pet supplies', 'Haircut', 'Misc purchase'],
}

INCOME_DETAILS = {
  'Salary': ['Bi-weekly paycheck', 'Monthly salary', 'Bonus payment', 'Overtime pay'],
  'Investments': ['Dividend payment', 'Stock sale profit', 'Interest income', '401k distribution'],
  'Miscellaneous': ['Cashback reward', 'Tax refund', 'Side gig income', 'Sold item'],
}

EXPENSE_RANGES = {
  'Housing': (800, 2500),
  'Food': (8, 150),
  'Transportation': (15, 200),
  'Entertainment': (10, 120),
  'Healthcare': (20, 350),
  'Utilities': (40, 250),
  'Shopping': (15, 400),
  'Miscellaneous': (5, 100),
}

INCOME_RANGES = {
  'Salary': (2000, 5500),
  'Investments': (50, 800),
  'Miscellaneous': (25, 500),
}

BUDGET_LIMITS = {
  'Housing': 2000,
  'Food': 600,
  'Transportation': 400,
  'Entertainment': 250,
  'Healthcare': 300,
  'Utilities': 350,
  'Shopping': 500,
  'Miscellaneous': 200,
}


def seed_database():
  app = create_app()

  with app.app_context():
    db.drop_all()
    db.create_all()

    demo_user = User(
      username='demo',
      email='demo@fintrack.app',
    )
    demo_user.set_password('demo1234')
    db.session.add(demo_user)
    db.session.flush()

    today = date.today()
    start_date = today - timedelta(days=365)
    transactions = []

    for _ in range(100):
      is_income = random.random() < 0.22
      if is_income:
        category = random.choice(list(INCOME_DETAILS.keys()))
        amount = round(random.uniform(*INCOME_RANGES[category]), 2)
        description = random.choice(INCOME_DETAILS[category])
        transaction_type = 'Income'
      else:
        category = random.choice(EXPENSE_CATEGORIES)
        amount = round(random.uniform(*EXPENSE_RANGES[category]), 2)
        description = random.choice(EXPENSE_DETAILS[category])
        transaction_type = 'Expense'

      days_offset = random.randint(0, 365)
      transaction_date = start_date + timedelta(days=days_offset)

      transactions.append(Transaction(
        user_id=demo_user.id,
        amount=amount,
        category=category,
        description=description,
        transaction_type=transaction_type,
        transaction_date=transaction_date,
      ))

    db.session.add_all(transactions)

    for category, limit in BUDGET_LIMITS.items():
      db.session.add(Budget(
        user_id=demo_user.id,
        category=category,
        monthly_limit=limit,
      ))

    db.session.commit()

    print('Database seeded successfully.')
    print('')
    print('Demo credentials:')
    print('  Username: demo')
    print('  Password: demo1234')
    print('')
    print(f'Created {len(transactions)} transactions and {len(BUDGET_LIMITS)} budgets.')


if __name__ == '__main__':
  seed_database()
