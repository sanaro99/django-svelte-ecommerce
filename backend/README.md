# Django Backend

RESTful API backend for django-svelte-ecommerce using Django, DRF, OAuth2, and PostgreSQL.

## Features

* OAuth2 authentication & role-based scopes (Django OAuth Toolkit)
* E-commerce models: Products, Categories, Orders, Customers
* Secure, scalable REST API (CRUD, filtering, pagination)
* OpenAPI/Swagger docs (`/docs/`)
* Ready for production (Postgres)

## Setup

Check the setup steps [here](../README.md#backend-setup)

## API Docs

* Swagger UI: [http://localhost:8000/docs/](http://localhost:8000/docs/)
* OpenAPI schema: [http://localhost:8000/schema/](http://localhost:8000/schema/)


## Production Deployment (Railway)

Check the deployment steps [here](../README.md#backend-railway)
---

**Directory structure:**

```
catalog/      # Product & category models, API for products, categories
sales/        # Order & customer models, API for orders, customers
ecomm/        # Project config, settings, URLs
accounts/     # User models, API for registration, login, logout, connection with OAuth2

```

---