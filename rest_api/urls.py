from .views import CategoryView, ProductView
from django.urls import path

urlpatterns = [
    path('category', CategoryView.as_view(), name='category_list'),
    path('category/add', CategoryView.as_view(), name='add_category'),
    path('product', ProductView.as_view(), name='product_list'),
    path('product/add', ProductView, name='add_product_mapped_to_category'),
    path('product/update', ProductView.as_view(), name='update_product'),
]

