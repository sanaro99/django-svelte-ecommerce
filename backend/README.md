# Django Backend

RESTful API backend for django-svelte-ecommerce using Django, DRF, OAuth2, and PostgreSQL.

## Features

* OAuth2 authentication & role-based scopes (Django OAuth Toolkit)
* E-commerce models: Products, Categories, Orders, Customers
* Secure, scalable REST API (CRUD, filtering, pagination)
* OpenAPI/Swagger docs (`/docs/`)
* Ready for production (Docker, Postgres)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # Set your DB and secret config
python manage.py migrate
python manage.py runserver
```

## Useful Commands

```bash
python manage.py createsuperuser
python manage.py seed_data    # (Optional) Seed test data
```

## API Docs

* Swagger UI: [http://localhost:8000/docs/](http://localhost:8000/docs/)
* OpenAPI schema: [http://localhost:8000/schema/](http://localhost:8000/schema/)

## Docker Usage

```bash
docker build -t ecommerce-backend .
docker run -p 8000:8000 ecommerce-backend
```

---

**Directory structure:**

```
catalog/      # Product & category models, API
sales/        # Order & customer models, API
ecomm/        # Project config, settings, URLs
```

---