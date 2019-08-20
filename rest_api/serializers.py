from rest_framework import serializers
from .models import Category, Product
import json



class CategorySerializer(serializers.ModelSerializer):
    child_list = serializers.ListField(
        child=serializers.CharField(),
    )
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'parent',
            'child_list'
        )

    def create(self, validated_data):
        if validated_data['parent']:
            parent_category = Category.objects.get(name=validated_data['parent'])
            if not parent_category.child_list:
                parent_category.child_list = list([validated_data['name']])
            else:
                parent_category.child_list.append(validated_data['name'])
            parent_category.save()
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.child_list = validated_data.get('child_list', instance.child_list)
        instance.save()
        return instance

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        categories = instance.child_list
        repr['child_list'] = []
        if isinstance(categories, list):
            for category in categories:
                repr['child_list'].append(category)
        return repr

    def toJSON(self, instance):
        return json.dumps(instance, default=lambda o: o.__dict__, sort_keys=True, indent=4)



class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'price',
            'currency',
            'category_list'
        )

    def create(self, validated_data):
        categories = validated_data.pop('category_list')
        product = Product(
            id=validated_data['id'],
            name=validated_data['name'],
            price=validated_data['price'],
            currency=validated_data['currency'])
        product.save()
        for name in categories:
            category = Category.objects.filter(name=name)
            if len(category) > 0:
                product.category_list.add(category[0].id )
        product.save()
        return product

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.price = validated_data.get('price', instance.price)
        instance.currency = validated_data.get('currency', instance.currency)
        instance.save()
        return instance

    def to_representation(self, instance):
        repr = super().to_representation(instance)
        categories = instance.category_list.all().values('name')
        repr['category_list'] = []
        for category in categories:
            repr['category_list'].append(category['name'])
        return repr