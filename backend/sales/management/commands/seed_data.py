from django.core.management.base import BaseCommand
from faker import Faker
from catalog.models import Category, Product
from sales.models import Customer, Order, OrderItem
from random import randint, uniform, choice
from django.utils.text import slugify

fake = Faker()


class Command(BaseCommand):
    help = "Seed the database with fake categories, products, customers, orders, and order items"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.NOTICE("Seeding database..."))

        # Clear old data (for dev only)
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Customer.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Create Categories
        categories = []
        for _ in range(6):
            name = fake.unique.word().capitalize()
            cat = Category.objects.create(
                name=name,
                slug=slugify(name),
            )
            categories.append(cat)

        # Create Products
        products = []
        for _ in range(50):
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

        # Create Customers
        customers = []
        for _ in range(25):
            customer = Customer.objects.create(
                email=fake.unique.email(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                phone=fake.phone_number()[:20],
            )
            customers.append(customer)

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