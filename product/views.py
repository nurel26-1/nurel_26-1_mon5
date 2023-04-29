from django.db.models import Avg, Count
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from product.models import Product, Review, Category, Tag
from product.serializers import ProductSerializer, CategorySerializer, ReviewSerializer, TagSerializer, \
    ProductValidateSerializer, CategoryValidateSerializer, ReviewValidateSerializer


@api_view(['GET', 'POST'])
def product_list_api_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        data_dict = ProductSerializer(products, many=True).data
        return Response(data=data_dict)
    elif request.method == 'POST':
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        title = serializer.validated_data.get('title')
        description = serializer.validated_data.get('description')
        price = serializer.validated_data.get('price')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
        product = Product.objects.create(title=title, description=description, price=price, category_id=category_id)
        product.tags.set(tags)
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
        serializer = ProductValidateSerializer(request.data)
        serializer.is_valid(raise_exception=True)
        product.title = serializer.validated_data.get('title')
        product.description = serializer.validated_data.get('description')
        product.price = serializer.validated_data.get('price')
        product.category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')
        product.tags.set(tags)
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
        serializer = ReviewValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
        text = serializer.validated_data.get('text')
        stars = serializer.validated_data.get('stars')
        product_id = serializer.validated_data.get('product_id')
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
        serializer = ReviewValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review.text = serializer.validated_data.get('text')
        review.stars = serializer.validated_data.get('stars')
        review.product_id = serializer.validated_data.get('product_id')
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
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name')
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
        serializer = CategoryValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category.name = serializer.validated_data.get('name')
        category.save()
        return Response(status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# @api_view(['GET', 'POST'])
# def tags_api_view(request):
#     if request.method == 'GET':
#         tags = Tag.objects.all()
#         data_dict = TagSerializer(tags, many=True).data
#         return Response(data=data_dict)
#     elif request.method == 'POST':
#         serializer = TagValidateSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         name = serializer.validated_data.get('name')
#         tag = Tag.objects.create()
#         tag.name.set(name)
#         tag.save()
#         return Response()


# @api_view(['GET', 'PUT', 'DELETE'])
# def tag_detail_api_view(request, id):
#     try:
#         tag = Tag.objects.get(id=id)
#     except Tag.DoesNotExist:
#         return Response(data={'errors': 'Tag does not exist'}, status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         data_dict = TagSerializer(tag, many=False).data
#         return Response(data_dict)
#     elif request.method == 'PUT':
#         serializer = TagSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         tag.name = serializer.validated_data.get('name')
#         tag.save()
#         return Response(status=status.HTTP_200_OK)
#     elif request.method == 'DELETE':
#         tag.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def products_reviews_api_view(request):
    products_reviews = Review.objects.all()
    avg_stars = Review.objects.aggregate(avg=Avg('stars'))
    data_dict = ReviewSerializer(products_reviews, many=True).data
    return Response(data=[data_dict, avg_stars])
