# catalog/views.py: API endpoints for Category and Product management
# - Secured via OAuth2 scopes (read:products/write:products) using MethodScopedTokenHasScope
# - Provides CRUD operations with filtering, search, and ordering

from rest_framework.viewsets import ModelViewSet
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from oauth2_provider.contrib.rest_framework import TokenHasScope, OAuth2Authentication
from rest_framework.permissions import IsAuthenticated # Import IsAuthenticated

# This custom permission class ensures that get_scopes correctly returns a list of scopes
# for the current request method when view.required_scopes is defined as a dictionary.
# This addresses an issue where the default TokenHasScope.get_scopes might incorrectly
# return the entire dictionary instead of the list of scopes for the specific method.
class MethodScopedTokenHasScope(TokenHasScope):
    """
    Custom permission class to handle OAuth2 scopes for different request methods.
    """
    def get_scopes(self, request, view):
        # Attempt to get the dictionary of required scopes from the view.
        # Default to an empty dictionary if 'required_scopes' is not present.
        required_scopes_attr = getattr(view, 'required_scopes', {})

        if isinstance(required_scopes_attr, dict):
            # If it's a dictionary, get the list of scopes for the current request method.
            # Default to an empty list if the method is not a key in the dictionary.
            return required_scopes_attr.get(request.method, [])
        elif isinstance(required_scopes_attr, (list, tuple)):
            # If 'required_scopes' was directly a list or tuple (less common for method-specific scopes),
            # return it as is. This maintains compatibility with TokenHasScope's original behavior
            # if required_scopes is not a dictionary.
            return list(required_scopes_attr)
        
        # If 'required_scopes' is not a dict, list, or tuple, or in case of other issues,
        # default to an empty list, indicating no specific scopes are required by this logic.
        return []

class CategoryViewSet(ModelViewSet):
    """
    Manage product categories for the store:
    - GET: list & retrieve (requires 'read:products')
    - POST/PUT/DELETE: create, update, delete (requires 'write:products')
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, MethodScopedTokenHasScope]
    required_scopes = {
        'GET': ['read:products'],
        'POST': ['write:products'],
        'PUT': ['write:products'],
        'DELETE': ['write:products'],
    }
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = "slug"  # SEO URLs

from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(ModelViewSet):
    """
    Manage products:
    - GET: list & retrieve (requires 'read:products')
    - POST/PUT/DELETE: create, update, delete (requires 'write:products')
    Supports search and ordering filters.
    """
    authentication_classes = [OAuth2Authentication]
    permission_classes = [IsAuthenticated, MethodScopedTokenHasScope]
    required_scopes = {
        'GET': ['read:products'],
        'POST': ['write:products'],
        'PUT': ['write:products'],
        'DELETE': ['write:products'],
    }
    queryset = Product.objects.select_related("category").all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = {
        'category': ['exact'],
        'stock': ['gte'],
    }
    search_fields = ["name", "description"]   # search by these fields
    ordering_fields = ["price", "created_at"] # allow ordering

    # /api/products/?category=3
    # /api/products/?price=499
    # /api/products/?search=laptop
    # /api/products/?ordering=price
