from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Review, Category
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer


@api_view(['GET'])
def product_list_api_view(request):
    products = Product.objects.all()
    data_dict = ProductSerializer(products, many=True).data
    return Response(data=data_dict)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    data_dict = ProductSerializer(product, many=False).data
    return Response(data=data_dict)


@api_view(['GET'])
def review_list_api_view(request):
    reviews = Review.objects.all()
    data_dict = ReviewSerializer(reviews, many=True).data
    return Response(data=data_dict)


@api_view(['GET'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    data_dict = ReviewSerializer(review, many=False).data
    return Response(data=data_dict)


@api_view(['GET'])
def category_list_api_view(request):
    categories = Category.objects.all()
    data_dict = CategorySerializer(categories, many=True).data
    return Response(data=data_dict)


@api_view(['GET'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    data_dict = CategorySerializer(category, many=False).data
    return Response(data=data_dict)
