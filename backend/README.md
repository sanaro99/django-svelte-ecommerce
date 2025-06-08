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


## Directory structure:

```
catalog/      # Product & category models, API for products, categories
sales/        # Order & customer models, API for orders, customers
ecomm/        # Project config, settings, URLs
accounts/     # User models, API for registration, login, logout, connection with OAuth2

```

## API Usage Examples
Below are sample `curl` commands demonstrating common API operations. Replace `<ACCESS_TOKEN>`, `<CLIENT_ID>`, `<CLIENT_SECRET>`, `<USERNAME>`, and `<PASSWORD>` as needed.

### 1. Obtain Access Token (Password Grant)
```bash
curl -X POST http://localhost:8000/o/token/ \
  -u <CLIENT_ID>:<CLIENT_SECRET> \
  -d grant_type=password \
  -d username=<USERNAME> \
  -d password=<PASSWORD>
```

### 2. Register New User
```bash
curl -X POST http://localhost:8000/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "pass123", "email": "alice@example.com"}'
```

### 3. Get Current User Profile
```bash
curl -X GET http://localhost:8000/accounts/user/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 4. List Categories
```bash
curl -X GET http://localhost:8000/api/categories/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 5. List Products (Paginated)
```bash
curl -X GET http://localhost:8000/api/products/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 6. Filter Products by Category
```bash
curl -X GET "http://localhost:8000/api/products/?category=1" \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 7. Create a New Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"items": [{"product": 2, "qty": 3},{"product":5,"qty":1}]}'
```

### 8. List Orders
```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 9. Order Details
```bash
curl -X GET http://localhost:8000/api/orders/1/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

### 10. Add Product to Cart
```bash
curl -X POST http://localhost:8000/api/cart/add/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 3, "qty": 2}'
```

### 11. Checkout Cart
```bash
curl -X POST http://localhost:8000/api/cart/checkout/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

---