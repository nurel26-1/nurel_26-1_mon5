from rest_framework import serializers
from product.models import Product, Review, Category


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title description price category'.split()


class ReviewSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Review
        fields = 'product text stars'.split()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
