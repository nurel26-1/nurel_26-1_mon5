from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Review, Category
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data_dict = ProductSerializer(products, many=True).data
        return Response(data=data_dict)
    elif request.method == 'POST':
        title = request.data.get('title')
        description = request.data.get('description')
        price = request.data.get('price')
        category_id = request.data.get('category_id')
        product = Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        product.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(data={'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data_dict = ProductSerializer(product, many=False).data
        return Response(data=data_dict)
    elif request.method == 'PUT':
        product.title = request.data.get('title')
        product.description = request.data.get('description')
        product.price = request.data.get('price')
        product.category_id = request.data.get('category_id')
        product.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        reviews = Review.objects.all()
        data_dict = ReviewSerializer(reviews, many=True).data
        return Response(data=data_dict)
    elif request.method == 'POST':
        text = request.data.get('text')
        stars = request.data.get('stars')
        product_id = request.data.get('product_id')
        review = Review.objects.create(text=text, stars=stars, product_id=product_id)
        review.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def review_detail_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(data={'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data_dict = ReviewSerializer(review, many=False).data
        return Response(data=data_dict)
    elif request.method == 'PUT':
        review.text = request.data.get('text')
        review.stars = request.data.get('stars')
        review.product_id = request.data.get('product_id')
        review.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def category_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        products_count = Category.objects.aggregate(count_products=Count('category'))
        data_dict = CategorySerializer(categories, many=True).data
        return Response(data=[data_dict, products_count])
    elif request.method == 'POST':
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        category.save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def category_detail_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(data={'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        data_dict = CategorySerializer(category, many=False).data
        return Response(data=data_dict)
    elif request.method == 'PUT':
        category.name = request.data.get('name')
        category.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def products_reviews_api_view(request):
    products_reviews = Review.objects.all()
    avg_stars = Review.objects.aggregate(avg=Avg('stars'))
    data_dict = ReviewSerializer(products_reviews, many=True).data
    return Response(data=[data_dict, avg_stars])
