from rest_framework.viewsets import ModelViewSet, ViewSet
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Customer, Order, OrderItem, Cart, CartItem
from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer, CartSerializer
from catalog.models import Product

class CustomerViewSet(ModelViewSet):
    permission_classes = [TokenHasReadWriteScope]
    required_scopes_for_read = ['read:orders']  # Assuming customer data is part of order context
    required_scopes_for_write = ['write:orders'] # Assuming customer data is part of order context
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(ModelViewSet):
    permission_classes = [TokenHasReadWriteScope]
    required_scopes_for_read = ['read:orders']
    required_scopes_for_write = ['write:orders']
    queryset = Order.objects.select_related("customer").prefetch_related("items__product").all()
    serializer_class = OrderSerializer

class OrderItemViewSet(ModelViewSet):
    permission_classes = [TokenHasReadWriteScope]
    required_scopes_for_read = ['read:orders']
    required_scopes_for_write = ['write:orders']
    queryset = OrderItem.objects.select_related("order", "product").all()
    serializer_class = OrderItemSerializer

class CartViewSet(ViewSet):
    """ViewSet for user cart: list, add items, remove items"""
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