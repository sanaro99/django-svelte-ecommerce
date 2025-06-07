from rest_framework.viewsets import ModelViewSet, ViewSet
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope, OAuth2Authentication
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
    permission_classes = [TokenHasReadWriteScope]
    required_scopes_for_read = ['read:orders']  # Assuming customer data is part of order context
    required_scopes_for_write = ['write:orders'] # Assuming customer data is part of order context
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(ModelViewSet):
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.select_related("customer").prefetch_related("items__product").all().order_by('-created_at')
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = {'status': ['exact'], 'created_at': ['gte']}
    ordering_fields = ['created_at']

    def get_queryset(self):
        # Only return orders for the logged-in user
        user = self.request.user
        return Order.objects.select_related("customer").prefetch_related("items__product").filter(customer__user=user).order_by('-created_at')

class OrderItemViewSet(ModelViewSet):
    permission_classes = [TokenHasReadWriteScope]
    required_scopes_for_read = ['read:orders']
    required_scopes_for_write = ['write:orders']
    queryset = OrderItem.objects.select_related("order", "product").all()
    serializer_class = OrderItemSerializer

class CartViewSet(ViewSet):
    """ViewSet for user cart: list, add items, remove items"""
    authentication_classes = [OAuth2Authentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

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
        cart.items.all().delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data)