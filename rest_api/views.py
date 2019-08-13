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
        category_serializer = None
        for category in categories:
            category_serializer = self.get_recursive_data(None, category)
        if not category_serializer:
            category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)

    def post(self, request):
        name = request.data.get('name', None)
        parent = request.data.get('parent', None)
        child_list = request.data.get('child_list', None)
        if name:
            serializer = CategorySerializer(
                data={
                    'name': name,
                    'parent': parent,
                    'child_list': child_list
                })
            if serializer.is_valid(raise_exception=True):
                category_saved = serializer.save()
            return Response({"success": "Category {} created successfully".format(category_saved.name)})
        else:
            return Response({"failure": "Error while creating the category"})

    def get_recursive_data(self, result, category):
        child_list = category.child_list
        if not child_list:
            return result
        for child in child_list:
            category = Category.object.get(name=child)
            if category:
                updated_child_list = result.data.get('child_list').append(category)
                result.data.update({'child_list': updated_child_list})
                child_categories = self.get_recursive_data(result.data, category)
                result = CategorySerializer(child_categories, many=True)
        return result



class ProductView(APIView):
    def get(self, request):
        category = request.data.get('category')
        if category:
            products = Product.objects.filter(category_list__contains=category)
        else:
            products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data)

    def post(self, request):
        name = request.data.get('name')
        price = int(request.data.get('price', 0))
        currency = request.data.get('currency', 'USD')
        category_name_list = request.data.get_list('category_list')
        category_list = []
        for name in category_name_list:
            category = Category.object.get(name=name)
            category_list.append(category)

        if not (name and price):
            return Response({"failure": "Please provide valid data"})
        serializer = ProductSerializer(
            data={
                'name': name,
                'price': price,
                'currency': currency,
                'category_list': category_list
            }
        )
        if serializer.is_valid(raise_exception=True):
            product_saved = serializer.save()
            return Response({"success":"Product {} created successfully".format(product_saved.name)})
        else:
            return Response({"failure": "Error while creating a product"})