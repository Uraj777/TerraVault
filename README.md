# TerraVault

### Production-Grade, Community-Driven Encyclopedia & Knowledge Platform

TerraVault is a clean-architecture, full-stack knowledge platform built using **Flask** and **Supabase PostgreSQL**. It combines structured, category-based encyclopedic articles (Wikipedia style) with a custom content management system (CMS), role-based access control, revision audit histories, and interactive metrics dashboards.

---

## 🛠️ Architecture & Core Components

```
TerraVault/
│
├── run.py                 # Application launcher
├── app/
│   ├── __init__.py        # App factory & blueprint register
│   ├── config.py          # Class-based configurations
│   ├── extensions.py      # SQLAlchemy, Migrate, Login, CSRF singletons
│   ├── models/            # SQLAlchemy database tables
│   ├── services/          # Business logic separation layer
│   ├── utils/             # Helper utilities (slugs, reading time, TOC anchors)
│   └── blueprints/        # Modular controller modules
│
├── templates/             # HTML layouts
├── static/                # Asset directories (images, styles, scripts)
├── migrations/            # Alembic schema tracking
└── seed.py                # Database seeder
```

* **Application Factory**: Configured using modular Flask Blueprints to cleanly separate routing files.
* **Separated Service Layer**: All database and computation logic (authentication, reading trackers, analytic lookups) is encapsulated inside the `services/` namespace.
* **Audit Revision Controls**: Modifying an article logs a new version history entry in `ArticleVersion` to preserve previous edits.
* **Dynamic Table of Contents**: Parses HTML headings on render, automatically injecting IDs and anchors for direct side-bar scroll links.
* **Admin Dashboard & Charts**: Displays interactive statistics metrics using Chart.js.

---

## 💻 Tech Stack

* **Core Framework**: Flask 3.0.3, Jinja2 templates
* **Authentication**: Flask-Login
* **ORM & Database**: SQLAlchemy, Alembic (via Flask-Migrate), Supabase PostgreSQL
* **Security & Forms**: Flask-WTF, CSRFProtect
* **Production Web Server**: Gunicorn
* **Containerization**: Docker, Docker Compose
* **Continuous Integration**: GitHub Actions CI

---

## ⚙️ Environment Variables

Copy `.env.example` to `.env` and fill in the required keys:

| Variable | Description | Default / Example |
| :--- | :--- | :--- |
| `FLASK_APP` | Main entrypoint | `run.py` |
| `FLASK_ENV` | Application environment | `development` / `production` |
| `SECRET_KEY` | Flask cryptographic secret | A secure random hex string |
| `DATABASE_URL` | Supabase PostgreSQL Connection String | `postgresql://user:pass@db.ref.supabase.co:5432/postgres` |

---

## 🚀 Local Installation & Execution

### 1. Traditional Method (Python Virtual Environment)
1. **Clone the repository** and navigate to the directory.
2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Apply Alembic migrations**:
   ```bash
   flask db upgrade
   ```
5. **Seed the database**:
   ```bash
   python seed.py
   ```
6. **Start the application**:
   * Development: `python run.py` (Flask Server)
   * Production: `gunicorn -b 127.0.0.1:8000 run:app`

### 2. Containerized Method (Docker Compose)
1. **Run build and boot**:
   ```bash
   docker-compose up --build
   ```
2. **Seed inside the container**:
   ```bash
   docker-compose exec web python seed.py
   ```

---

## 🐳 Docker Deployment

To build and run the Docker image independently:
```bash
docker build -t terravault:latest .
docker run -d -p 5000:5000 --env-file .env terravault:latest
```

---

## 📝 Render & Supabase Deployment Checklist

### Step 1: Set up Supabase PostgreSQL
1. Sign up on [Supabase](https://supabase.com/).
2. Create a new project. Note your **Database Password**.
3. Go to **Project Settings > Database > Connection strings** and copy the **URI** (choose the **Transaction Pooler** mode, port `6543`, for serverless-friendly connection management).
4. Replace `postgres://` prefix with `postgresql://` (Render/Flask require the modern dialect).

### Step 2: Set up Web Service on Render
1. Sign up on [Render](https://render.com/).
2. Click **New +** and select **Web Service**.
3. Connect your GitHub Repository.
4. Set the following parameters:
   * **Name**: `terravault`
   * **Region**: Choose closest to you
   * **Branch**: `deployment-ready` (or `main`)
   * **Runtime**: `Python 3`
   * **Build Command**: `pip install -r requirements.txt && flask db upgrade && python seed.py`
   * **Start Command**: `gunicorn run:app`
5. Go to **Advanced > Environment Variables** and add:
   * `SECRET_KEY` = *[Your Secure Hex Secret]*
   * `DATABASE_URL` = *[Your Supabase Connection URI]*
   * `FLASK_ENV` = `production`
6. Click **Create Web Service**.
