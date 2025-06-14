from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    category    = models.ForeignKey(
        Category,
        related_name="products",
        on_delete=models.CASCADE,
    )
    name        = models.CharField(max_length=180)
    slug        = models.SlugField(max_length=180, unique=True, blank=True)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    stock       = models.PositiveIntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="specifications",
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.name}: {self.name}={self.value}"


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        related_name="images",
        on_delete=models.CASCADE,
    )
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.name} image: {self.url}"