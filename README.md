# FinTrack

A production-quality personal finance management web application built with Flask, SQLite, SQLAlchemy, Bootstrap 5, and Chart.js.

## Features

- **Authentication** — Register, login, logout with password hashing and session management
- **Dashboard** — Financial summary cards, expense breakdown, monthly trends, and budget overview
- **Transactions** — Full CRUD with pagination, search, category/date filters, and sorting
- **Budgets** — Set monthly limits by category with progress bars and over-budget warnings
- **Analytics** — Spending statistics, category rankings, trend analysis, and budget utilization charts
- **Profile** — Update email and change password

## Tech Stack

- Python / Flask
- SQLite + SQLAlchemy ORM
- Flask-Login for session management
- Flask-WTF for CSRF protection and form validation
- Bootstrap 5 + Bootstrap Icons
- Chart.js for interactive visualizations

## Installation

### Prerequisites

- Python 3.10 or higher
- pip

### Setup

1. Clone or download the project and navigate to the directory:

```bash
cd fintrack
```

2. Create and activate a virtual environment (recommended):

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Database Setup

Seed the database with a demo user, 100 realistic transactions, and sample budgets:

```bash
python seed.py
```

This creates a SQLite database at `database/fintrack.db`.

## Running the Application

Start the development server:

```bash
python run.py
```

Open your browser to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Demo Credentials

| Field    | Value        |
|----------|--------------|
| Username | `demo`       |
| Password | `demo1234`   |

You can also register a new account from the registration page.

## Project Structure

```
fintrack/
├── app/
│   ├── __init__.py          # Application factory
│   ├── extensions.py        # Flask extensions
│   ├── forms.py               # WTForms definitions
│   ├── services.py            # Business logic & analytics
│   ├── models/
│   │   ├── user.py
│   │   ├── transaction.py
│   │   └── budget.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── transactions.py
│   │   ├── budgets.py
│   │   ├── analytics.py
│   │   └── profile.py
│   ├── templates/
│   └── static/
│       ├── css/
│       └── js/
├── database/
│   └── fintrack.db          # Created after seeding
├── config.py
├── seed.py
├── run.py
├── requirements.txt
└── README.md
```

## Security

- Passwords hashed with Werkzeug
- CSRF protection on all forms via Flask-WTF
- Server-side input validation
- SQLAlchemy ORM prevents SQL injection
- Users can only access their own data via `user_id` filtering on all queries

## License

MIT
