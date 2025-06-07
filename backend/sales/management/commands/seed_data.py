from django.core.management.base import BaseCommand
from faker import Faker
from catalog.models import Category, Product, ProductSpecification, ProductImage
from django.contrib.auth import get_user_model
from sales.models import Customer, Order, OrderItem, Cart, CartItem
from random import randint, uniform, choice, sample
from django.utils.text import slugify

fake = Faker()
User = get_user_model()

# Realistic specification keys
SPEC_NAMES = [
    "Color", "Weight", "Dimensions", "Material", "Manufacturer",
    "Model Number", "Battery Life", "Warranty", "Connectivity", "Display Size"
]

def random_image_url():
    return f"https://picsum.photos/seed/{randint(1, 1000)}/400/300"

class Command(BaseCommand):
    help = "Seed the database with fake categories, products, customers, orders, and order items"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding database..."))

        # Clear old data (for dev only)
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        Product.objects.all().delete()
        ProductSpecification.objects.all().delete()
        Category.objects.all().delete()
        ProductImage.objects.all().delete()
        # Clear cart data
        CartItem.objects.all().delete()
        Cart.objects.all().delete()
        # Clear old auth users
        User.objects.all().delete()

        # Create Categories
        categories = []
        for _ in range(6):
            name = fake.unique.word().capitalize()
            cat = Category.objects.create(
                name=name,
                slug=slugify(name),
            )
            categories.append(cat)

        # Create test users
        User.objects.create_superuser(username='testadmin', email='testadmin@example.com', password='testpassword')
        User.objects.create_superuser(username='testcustomer', email='testcustomer@example.com', password='testpassword')

        # Create Products
        products = []
        for _ in range(500):
            # Generate a random product name
            name = fake.unique.sentence(nb_words=3).replace(".", "")
            product = Product.objects.create(
                name=name,
                slug=slugify(name),
                description=fake.paragraph(),
                price=round(uniform(20, 3000), 2),
                stock=randint(10, 250),
                category=choice(categories),
            )
            products.append(product)
            # Seed product specifications
            num_specs = randint(3, 6)
            spec_keys = sample(SPEC_NAMES, num_specs)
            for key in spec_keys:
                value = fake.word().capitalize()
                ProductSpecification.objects.create(product=product, name=key, value=value)
            # Seed product images
            for _ in range(3):
                ProductImage.objects.create(product=product, url=random_image_url())

        # Create Users and associated Customers
        customers = []
        for _ in range(25):
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.unique.email()
            username = slugify(email.split('@')[0]) + str(randint(100, 999))
            user = User.objects.create_user(
                username=username,
                email=email,
                password='password',
                first_name=first_name,
                last_name=last_name,
            )
            # Populate customer profile
            customer = Customer.objects.get(user=user)
            customer.phone = fake.phone_number()[:20]
            customer.street_address = fake.street_address()
            customer.city = fake.city()
            customer.state = fake.state()
            customer.postal_code = fake.postcode()
            customer.country = fake.country()
            customer.save()
            customers.append(customer)
        # Promote random customers to admin
        for cust in sample(customers, 5):
            u = cust.user
            u.is_staff = True
            u.is_superuser = True
            u.save()

        # Create Orders and OrderItems
        status_choices = ["pending", "paid", "shipped", "completed", "cancelled"]
        for _ in range(40):
            customer = choice(customers)
            order = Order.objects.create(
                customer=customer,
                status=choice(status_choices),
            )

            # For each order, create 1-5 order items
            num_items = randint(1, 5)
            order_products = fake.random_elements(elements=products, length=num_items, unique=True)
            for product in order_products:
                qty = randint(1, 4)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    qty=qty,
                    price=product.price,
                )

        self.stdout.write(self.style.SUCCESS("Seeding complete!"))