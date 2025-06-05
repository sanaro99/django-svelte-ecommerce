from rest_framework.viewsets import ModelViewSet
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"  # SEO URLs

from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["category", "price"]  # filter by exact category or price
    search_fields = ["name", "description"]   # search by these fields
    ordering_fields = ["price", "created_at"] # allow ordering

    # /api/products/?category=3
    # /api/products/?price=499
    # /api/products/?search=laptop
    # /api/products/?ordering=price
