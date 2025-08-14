# BrandMetrics

BrandMetrics is a Django application for tracking brand performance, employee metrics, and order processing. Features include team chat and analytics. This README covers installation via Docker, pip, or `uv`.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [1. Using Docker](#1-using-docker)
  - [2. Using pip](#2-using-pip)
  - [3. Using uv](#3-using-uv)
- [Running the Application](#running-the-application)
- [Collecting Static Files](#collecting-static-files)
- [Running Scripts](#running-scripts)
- [Project Structure](#project-structure)

---

## Prerequisites

- Python 3.13
- pip
- uv (optional)
- Docker (optional)

---

## Installation

### 1. Using Docker

1. Build the Docker image:

```bash
docker build -t brandmetrics .
````

2. Run the container:

```bash
docker run -p 8000:8000 brandmetrics
```

3. Access the app at: [http://localhost:8000](http://localhost:8000)


---

### 2. Using pip

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

2. Install dependencies:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

3. Apply migrations:

```bash
python manage.py migrate
```

4. Collect static files:

```bash
python manage.py collectstatic --noinput
```

5. Run the development server:

```bash
python manage.py runserver
```

---

### 3. Using uv

1. Install uv:

```bash
curl -sSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"
```

2. Generate `requirements.txt` (optional):

```bash
uv pip compile pyproject.toml -o requirements.txt
```

3. Install dependencies:

```bash
uv pip install -e .
```

4. Apply migrations and collect static files:

```bash
python manage.py migrate
python manage.py collectstatic --noinput
```

5. Run the development server:

```bash
python manage.py runserver
```

---

## Running Scripts

Scripts are located under `scripts/`:

* `load_employees.py` — Load employee data
* `load_orders.py` — Load order data
* `load_payouts.py` — Load payout data

Example:

```bash
python scripts/load_employees.py
```

---

## Project Structure

```
brandmetrics/
├── brandmetrics/           # Django project settings
│   ├── chat/               # Django app
│   ├── db.sqlite3          # SQLite database
│   ├── manage.py           # Django management script
│   └── templates/          # HTML templates
├── Dockerfile
├── pyproject.toml          # uv/Poetry dependencies
├── requirements.txt
└── scripts/                # Utility scripts
```

---

## Notes

* For development, `python manage.py runserver` is sufficient.
* For production, use Gunicorn or another WSGI server.
* `uv` ensures deterministic dependency installs across environments.
