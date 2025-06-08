# Catalog App Test Suite

## Unit Tests
- **test_models.py**
  - `CategoryModelTest.test_str`: verifies `Category.__str__` returns the category name.
  - `ProductModelTest.test_str`: verifies `Product.__str__` returns the product name.
- **test_serializers.py**
  - `CategorySerializerTest.test_serialization`: checks serialized `id` and `name` fields.
  - `ProductSerializerTest.test_serialization`: checks serialized `id`, `name`, `category` (id), `price`, and `stock`.

## API Integration Tests
- **test_views.py**
  - **CategoryViewSetTest**
    - tests unauthorized access without `read:products`.
    - `test_list`: GET `/api/categories/` requires `read:products` and returns a list.
    - `test_retrieve`: GET `/api/categories/{slug}/` returns detail.
    - `test_create_update_delete`: POST/PUT/PATCH/DELETE flows require `write:products`.
    - validates filtering, searching, and ordering behavior.
    - error handling for invalid data (e.g., duplicate slug).
  - **ProductViewSetTest**
    - `test_list` and `test_retrieve` with `read:products`.
    - filtering by `category` and `stock__gte`, search (`name`, `description`), ordering (`price`, `created_at`).
    - create/update/delete with `write:products`.
    - error handling for invalid payloads.

## Running Tests
Activate your virtual environment from `backend/`:

```bash
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows
```

And run:
```bash
python manage.py test catalog
```