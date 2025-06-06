from rest_framework.viewsets import ModelViewSet
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope, TokenHasScope
from .models import Customer, Order, OrderItem
from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer

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