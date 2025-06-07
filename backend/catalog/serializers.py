from rest_framework import serializers
from .models import Category, Product, ProductSpecification

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class ProductSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductSpecification
        fields = ["name", "value"]

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"