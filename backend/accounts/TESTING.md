# Accounts App Test Suite

## Unit Tests
- **RegisterView Tests** (in `tests.py`)
  - test successful registration with valid credentials.
  - test duplicate username registration fails.
  - test password strength validation errors.
- **UserDetailView Tests** (in `tests.py`)
  - test GET `/accounts/user/` requires `read:customers` and returns current user profile.
  - test PATCH `/accounts/user/` requires `write:customers`, partial updates profile.

## Integration Tests
- **End-to-End User Flows**
  - registration -> login -> profile retrieval.
  - profile update persistence.

## Running Tests
Activate your virtual environment from `backend/`:

```bash
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows
```

And run:
```bash
python manage.py test accounts
```