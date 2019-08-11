from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
# Create your views here.

class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        for category in categories:
            category_serializer = self.get_recursive_data(None, category)
        return Response(category_serializer.data)

    def post(self):
        pass

    def get_recursive_data(self, result, category):
        child_list = category['child_list']
        if not child_list:
            result.update({'child_list': None})
            return result
        for child in child_list:
            category = Category.object.filter(name=child)
            if category:
                child_categories = self.get_recursive_data(result.data, category)
                result = CategorySerializer(child_categories, many=True)
        return result


class ProductView(APIView):
    def get(self, request):
        category = request.get('category')
        if category:
            products = Product.objects.filter(category_list__contains=category)
        else:
            products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data)

    def post(self):
        pass