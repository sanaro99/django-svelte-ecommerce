from rest_framework.viewsets import ModelViewSet
from .models import Customer, Order, OrderItem
from .serializers import CustomerSerializer, OrderSerializer, OrderItemSerializer

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.select_related("customer").prefetch_related("items__product").all()
    serializer_class = OrderSerializer

class OrderItemViewSet(ModelViewSet):
    queryset = OrderItem.objects.select_related("order", "product").all()
    serializer_class = OrderItemSerializer