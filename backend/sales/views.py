# sales/views.py: API endpoints for Customer, Order, OrderItem, and Cart management
# - Secured via OAuth2 scopes (read:customers/write:customers, read:orders/write:orders, read:cart/write:cart) using MethodScopedTokenHasScope
# - Querysets filtered to request.user for Customer, Orders, and OrderItems
# - CartViewSet offers custom cart actions (list, add, remove, checkout) scoped to request.user

from rest_framework.viewsets import ModelViewSet, ViewSet
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from catalog.views import MethodScopedTokenHasScope
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from .models import Customer, Order, OrderItem, Cart, CartItem
from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer, CartSerializer
from catalog.models import Product
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

class CustomerViewSet(ModelViewSet):
    """
    manage the Customer profile for the authenticated user
    """
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, MethodScopedTokenHasScope]
    required_scopes = {
        'GET': ['read:customers'],
        'POST': ['write:customers'],
        'PUT': ['write:customers'],
        'PATCH': ['write:customers'],
        'DELETE': ['write:customers'],
    }
    def get_queryset(self):
        # enforce consistent ordering to satisfy pagination requirements
        return Customer.objects.filter(user=self.request.user).order_by('id')
    serializer_class = CustomerSerializer

class OrderViewSet(ModelViewSet):
    """
    List and manipulate Orders belonging to the authenticated user
    """
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, MethodScopedTokenHasScope]
    required_scopes = {
        'GET': ['read:orders'],
        'POST': ['write:orders'],
        'PUT': ['write:orders'],
        'PATCH': ['write:orders'],
        'DELETE': ['write:orders'],
    }
    def get_queryset(self):
        return Order.objects.select_related("customer").prefetch_related("items__product").filter(customer__user=self.request.user).order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {'status': ['exact'], 'created_at': ['gte']}
    ordering_fields = ['created_at']

class OrderItemViewSet(ModelViewSet):
    """
    manage OrderItems within the authenticated user's Orders
    """
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, MethodScopedTokenHasScope]
    required_scopes = {
        'GET': ['read:orders'],
        'POST': ['write:orders'],
        'PUT': ['write:orders'],
        'PATCH': ['write:orders'],
        'DELETE': ['write:orders'],
    }
    def get_queryset(self):
        # enforce consistent ordering to satisfy pagination requirements
        return OrderItem.objects.select_related("order", "product").filter(order__customer__user=self.request.user).order_by('id')
    serializer_class = OrderItemSerializer

class CartViewSet(ViewSet):
    """
    custom actions (list, add, remove, checkout) for the authenticated user's cart
    """
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, MethodScopedTokenHasScope]
    required_scopes = {
        'GET': ['read:cart'],
        'POST': ['write:cart'],
    }

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def add(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product_id = request.data.get('product_id')
        qty = int(request.data.get('qty', 1))
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Invalid product_id'}, status=400)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={'price': product.price, 'qty': qty}
        )
        if not created:
            item.qty = qty
            item.price = product.price
            item.save()
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    def remove(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item_id = request.data.get('item_id')
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
            item.delete()
        except CartItem.DoesNotExist:
            return Response({'error': 'Invalid item_id'}, status=400)
        return Response(CartSerializer(cart).data)

    @action(detail=False, methods=['post'])
    def checkout(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        if not cart.items.exists():
            return Response({'error': 'Cart is empty'}, status=400)
        customer = request.user.customer
        order = Order.objects.create(customer=customer, status='pending')
        for item in cart.items.all():
            OrderItem.objects.create(order=order, product=item.product, qty=item.qty, price=item.price)
            # decrement product stock
            product = item.product
            product.stock -= item.qty
            product.save()
        cart.items.all().delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data)