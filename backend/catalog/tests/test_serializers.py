from django.test import TestCase
from catalog.models import Category, Product
from catalog.serializers import CategorySerializer, ProductSerializer

class CategorySerializerTest(TestCase):
    def test_serialization(self):
        cat = Category.objects.create(name="Electronics")
        data = CategorySerializer(cat).data
        self.assertEqual(data["id"], cat.id)
        self.assertEqual(data["name"], "Electronics")

class ProductSerializerTest(TestCase):
    def setUp(self):
        self.cat = Category.objects.create(name="Books")
    def test_serialization(self):
        prod = Product.objects.create(name="Novel", category=self.cat, price=19.99, stock=5)
        data = ProductSerializer(prod).data
        self.assertEqual(data["id"], prod.id)
        self.assertEqual(data["name"], "Novel")
        self.assertEqual(data["category"], self.cat.id)
        self.assertEqual(str(data["price"]), "19.99")
        self.assertEqual(data["stock"], 5)
