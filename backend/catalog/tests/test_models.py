from django.test import TestCase
from catalog.models import Category, Product

class CategoryModelTest(TestCase):
    def test_str(self):
        cat = Category.objects.create(name="Electronics")
        self.assertEqual(str(cat), "Electronics")

class ProductModelTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Books")

    def test_str(self):
        prod = Product.objects.create(name="Novel", category=self.cat, price=19.99, stock=1)
        self.assertEqual(str(prod), "Novel")
