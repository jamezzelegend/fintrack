# FinTrack

FinTrack is a personal finance management application that allows users to track transactions, manage budgets, and visualize spending trends through interactive dashboards and analytics.

The project demonstrates full-stack web development with Flask, SQLAlchemy, authentication, database design, analytics reporting, and cloud deployment.

**[Live Demo](https://fintrack-1-is4j.onrender.com)** &nbsp;·&nbsp; Python 3.12 &nbsp;·&nbsp; Flask 3.0

---

## Features

- **Dashboard** — Summary of income, expenses, and net balance with interactive charts
- **Transactions** — Add, edit, and delete transactions with search, category filters, date range filters, and multi-column sorting
- **Budgets** — Set monthly spending limits per category with real-time usage progress bars and over-budget alerts
- **Analytics** — Spending breakdowns, category rankings, 12-month income vs expense trends, and budget utilisation charts
- **Authentication** — Register, log in, and log out with secure password hashing and persistent sessions
- **Profile** — Update email address and change password

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Flask 3.0 |
| Database | PostgreSQL (production), SQLite (local dev) |
| ORM | SQLAlchemy via Flask-SQLAlchemy |
| Auth | Flask-Login |
| Forms | Flask-WTF, WTForms |
| Frontend | Bootstrap 5, Bootstrap Icons, Chart.js |
| Deployment | Render (Gunicorn) |

---

## Screenshots

> Add screenshots here after deployment.

| Dashboard | Transactions | Analytics |
|---|---|---|
| *(screenshot)* | *(screenshot)* | *(screenshot)* |

---

## Architecture

```
fintrack/
├── app/
│   ├── __init__.py        # Application factory
│   ├── extensions.py      # Flask extension instances
│   ├── forms.py           # WTForms form definitions
│   ├── services.py        # Business logic and analytics queries
│   ├── models/            # SQLAlchemy models (User, Transaction, Budget)
│   └── routes/            # Blueprints (auth, dashboard, transactions, budgets, analytics, profile)
├── config.py              # Config class (reads SECRET_KEY, DATABASE_URL from env)
├── run.py                 # App entry point
├── seed.py                # Dev seed script (demo user + sample data)
└── requirements.txt
```

The app uses a factory pattern (`create_app()`) with blueprints for each feature area. All database tables are created automatically on first boot via `db.create_all()`.

---

## Local Setup

**Prerequisites:** Python 3.10+

```bash
git clone https://github.com/jamezzelegend/fintrack.git
cd fintrack

python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

pip install -r requirements.txt
python run.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

To seed the database with a demo account and 100 sample transactions:

```bash
python seed.py
```

Demo credentials: username `demo` / password `demo1234`

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Yes | Flask session signing key. Use a long random string in production. |
| `DATABASE_URL` | No | Database connection string. Defaults to local SQLite if not set. Render Postgres URLs (`postgres://`) are normalised automatically. |

For local development, these can be set in a `.env` file (not committed to source control).

---

## Resume Highlights

- Implemented a Flask application factory pattern with Blueprint-based routing, separating concerns across six feature modules
- Designed a relational schema with three models (User, Transaction, Budget) using SQLAlchemy ORM with foreign keys, unique constraints, and check constraints
- Built a server-side analytics layer (`services.py`) computing monthly trends, category breakdowns, and savings rate using SQLAlchemy aggregate queries — no external analytics library
- Secured all routes with Flask-Login session management, CSRF protection on every form via Flask-WTF, and per-query `user_id` filtering to prevent cross-user data access
- Deployed to Render using Gunicorn with PostgreSQL, handling the SQLAlchemy `postgres://` → `postgresql://` scheme difference between Render's database URLs and SQLAlchemy 2.x
