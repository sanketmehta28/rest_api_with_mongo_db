# from django.db import models

import ast
from djongo import models

class ListField(models.CharField):
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        return value



# Create your models here.
class Category(models.Model):
    id = models.IntegerField(default=1, null=False, primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=False)
    parent = models.CharField(max_length=100, null=True, blank=True)
    child_list = ListField(max_length=1000, null=True, blank=True, default=None)
    objects = models.DjongoManager()

    def __str__(self):
        return self.name



class Product(models.Model):
    id = models.IntegerField(default=1, null=False, primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=False)
    price = models.IntegerField(default=0, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, default='USD', blank=True)
    category_list = models.ManyToManyField(
        Category,
        related_name='categories',
        blank=True,
    )

    objects = models.DjongoManager()

    def __str__(self):
        return self.name
