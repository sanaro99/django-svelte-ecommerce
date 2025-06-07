from django.contrib import admin
# Register your models here.
# Register cart models
from .models import Cart, CartItem

admin.site.register(Cart)
admin.site.register(CartItem)
