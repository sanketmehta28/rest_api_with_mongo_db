
from django.db.models import Max, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
# Create your views here.

class CategoryView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        category_serializer = CategorySerializer(categories, many=True)
        return Response(category_serializer.data)

    def post(self, request):
        id = request.data.get('id', 1)
        name = request.data.get('name', None)
        parent = request.data.get('parent', None)
        child_list = request.data.get('child_list', [])
        if name:
            data = {'name': name, 'parent': parent, 'child_list': child_list}
            if not Category.objects.exists():
                data['id'] = id
            else:
                data['id'] = Category.objects.aggregate(Max('id'))['id__max'] + 1
            serializer = CategorySerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                category_saved = serializer.save()
            return Response({"success": "Category {} created successfully".format(category_saved.name)})
        else:
            return Response({"failure": "Error while creating the category"})



class ProductView(APIView):
    def get(self, request):
        category = request.GET.get('category')
        if category:
            products = Product.objects.filter(Q(category_list__name__icontains=category))
        else:
            products = Product.objects.all()
        product_serializer = ProductSerializer(products, many=True)
        return Response(product_serializer.data)

    def post(self, request):
        id = request.data.get('id', 1)
        name = request.data.get('name')
        price = int(request.data.get('price', 0))
        currency = request.data.get('currency', 'USD')
        category_name_list = request.data.get('category_list')
        category_list = []
        if category_name_list:
            for category_name in category_name_list:
                category = Category.objects.filter(name=category_name).values('pk')
                if len(category) > 0:
                    category_list.append(category[0]['pk'])
        else:
            empty_list = Category.objects.filter(name=None).values('name')
            category_list.append(empty_list)
        data = {
            'name': name,
            'price': price,
            'currency': currency,
            'category_list': category_list
        }
        if not Product.objects.exists():
            data['id'] = id
        else:
            data['id'] = Product.objects.aggregate(Max('id'))['id__max'] + 1
        if not (name and price):
            return Response({"failure": "Please provide valid data"})
        serializer = ProductSerializer(
            data=data
        )
        if serializer.is_valid(raise_exception=True):
            product_saved = serializer.save()
            return Response({"success":"Product {} created successfully".format(product_saved.name)})
        else:
            return Response({"failure": "Error while creating a product"})

    def put(self, request):
        id = request.data.get('id')
        name = request.data.get('name')
        price = int(request.data.get('price', 0))
        currency = request.data.get('currency', 'USD')
        new_name = request.data.get('new_name')
        if id:
            product = Product.objects.filter(id=id)
        elif name:
            product = Product.objects.filter(name=name)
        data = {'price': price, 'currency': currency}
        if new_name:
            data['name'] = new_name

        if len(product) > 0:
            serializer = ProductSerializer(
                product[0],
               data=data,
                partial=True
            )
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response({"success":"product is updated successfully"})
            else:
                return Response({"failure":"failed to update an instance"})
        return Response({"failure": "No product available with this name and id"})