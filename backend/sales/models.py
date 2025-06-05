from django.db import models
from catalog.models import Product

class Customer(models.Model):
    email       = models.EmailField(unique=True)
    first_name  = models.CharField(max_length=80)
    last_name   = models.CharField(max_length=80)
    phone       = models.CharField(max_length=20, blank=True)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("paid", "Paid"),
        ("shipped", "Shipped"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    customer    = models.ForeignKey(
        Customer,
        related_name="orders",
        on_delete=models.CASCADE,
    )
    status      = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default="pending",
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} – {self.status}"

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())


class OrderItem(models.Model):
    order   = models.ForeignKey(
        Order,
        related_name="items",
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    qty     = models.PositiveIntegerField()
    price   = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("order", "product")

    @property
    def subtotal(self):
        return self.qty * self.price