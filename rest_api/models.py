# from django.db import models
from djongo import models


# Create your models here.
class Category(models.Model):
    id = models.IntegerField(default=1, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    child_list = models.ListField(models.CharField(max_length=100, null=True), null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.IntegerField(default=1, null=False, primary_key=True)
    name = models.CharField(max_length=100, null=False)
    price = models.IntegerField(default=0, null=True)
    currency = models.CharField(max_length=10, null=True, default='USD')
    category_list = models.ArrayReferenceField(
        to=Category,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
