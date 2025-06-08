# Sales App Test Suite

## Unit Tests
- **test_models.py**
  - CustomerModelTest
    - `test_customer_profile_autocreation_and_str`: verifies a `Customer` is auto-created for each `User` and `__str__` returns "First Last" as name.
  - OrderModelTest
    - `test_str`: ensures `Order.__str__` formats as `Order <id> – <status>`.
    - `test_total_amount`: checks the `total_amount` property sums `OrderItem.subtotal`.
  - OrderItemModelTest
    - `test_subtotal`: validates `OrderItem.subtotal` equals `qty * price`.
  - CartModelTest
    - `test_str`: confirms `Cart.__str__` returns "Cart for <username>".
  - CartItemModelTest
    - `test_subtotal`: validates `CartItem.subtotal` equals `qty * price`.

## Serializer Tests
- **test_serializers.py**
  - UserSerializerTest: checks serialized fields `id`, `username`, `email`, `first_name`, `last_name`.
  - CustomerSerializerTest
    - `test_read`: read-only `user` object present, `user_id` hidden.
    - `test_write`: performs partial update on existing `Customer`, writes `phone` field.
  - OrderItemSerializerTest
    - `test_representation`: verifies `qty`, `price`, `subtotal`, and nested `product` in output.
  - OrderSerializerTest
    - `test_items_and_total`: ensures nested `items` list and `total_amount` computed.
  - CartItemSerializerTest
    - `test_representation`: verifies `qty`, `price`, `subtotal`, and nested `product`.
  - CartSerializerTest
    - `test_total_amount`: checks `total_amount` as sum of item subtotals.

## API View Tests
- **test_views.py**
  - **CartCheckoutTest**
    - Setup adds `CartItem` and verifies stock, cart clearing, and empty-cart error on checkout.
    - `test_checkout_decrements_stock`, `test_cart_cleared_after_checkout`, `test_checkout_empty_cart`.
  - **CartFlowTest**
    - Tests unauthorized (401) and authorized `list`, `add`, `remove` flows with proper OAuth2 scopes (`read:cart`, `write:cart`).
  - **CheckoutResponseTest**
    - `test_payload`: validates JSON response contains `items` array and correct `total_amount`.
  - **OrderViewSetTest**
    - `test_list_and_retrieve`: enforces `read:orders`, lists own orders, returns 404 for others.
  - **CustomerViewSetTest**
    - `test_get_and_update`: checks `read:customers` allows GET, `write:customers` allows PATCH, denies without scope.
  - **OrderItemViewSetTest**
    - `test_list_and_retrieve`: enforces `read:orders`, lists and retrieves `OrderItem` belonging to user.

## Running Tests
Activate your virtual environment from `backend/`:

```bash
source .venv/bin/activate # Linux/Mac
.venv\Scripts\activate # Windows
```

And run:
```bash
python manage.py test sales
```