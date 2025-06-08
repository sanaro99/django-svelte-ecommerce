# Ecomm (Project) Test Suite

## Accounts App Tests

Read the [accounts/TESTING.md](../accounts/TESTING.md) file for more info.

## Catalog App Tests

Read the [catalog/TESTING.md](../catalog/TESTING.md) file for more info.

## Sales App Tests

Read the [sales/TESTING.md](../sales/TESTING.md) file for more info.

## Integration Tests
- The `ecomm` URLs include routed endpoints for catalog, sales, and accounts.
- No dedicated tests here; tests reside in each app.

## Ecomm (Project) End-to-End & Smoke Tests

## API Entry Points
- **APIRootTest**: ensures `/api/` lists all registered routes.
- **SchemaAndDocsTest**: validates OpenAPI schema at `/schema/` and docs at `/docs/`.

## OAuth2 Flow
- **OAuth2TokenFlowTest**: password grant token retrieval with full scope set.

## E2E Shopping Flow
- **E2EShoppingFlowTest**: covers:
  1. user registration `POST /accounts/register/`
  2. OAuth2 token request `POST /o/token/`
  3. list empty cart `GET /api/cart/`
  4. add product to cart `POST /api/cart/add/`
  5. checkout `POST /api/cart/checkout/`
  6. verify order in `GET /api/orders/`

## Running Tests
Activate your virtual environment from `backend/`:

```bash
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows
```

And run:
```bash
python manage.py test ecomm
```