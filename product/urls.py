from django.urls import path
from product import views

urlpatterns = [
    path('categories/', views.category_list_api_view),
    path('categories/<int:id>/', views.category_detail_api_view),
    path('products/', views.product_list_api_view),
    path('products/<int:id>/', views.product_detail_api_view),
    path('reviews/', views.review_list_api_view),
    path('reviews/<int:id>/', views.review_detail_api_view),
    path('products/reviews/', views.products_reviews_api_view)
]
