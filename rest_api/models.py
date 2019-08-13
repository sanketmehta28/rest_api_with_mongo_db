# from django.db import models
from djongo import models
import ast
from pytz import unicode


class ListField(models.CharField):
    # __metaclass__ = models.SubfieldBase
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

        return unicode(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

# Create your models here.
class Category(models.Model):
    id = models.IntegerField(default=1, null=False, primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=False)
    parent = models.CharField(max_length=100, null=True, blank=True)
    # child_list = models.ListField(models.CharField, null=True, blank=True, default=None)
    child_list = ListField(blank=True, null=True, default=None, max_length=500)
    objects = models.DjongoManager()

    def __str__(self):
        return self.name



class Product(models.Model):
    id = models.IntegerField(default=1, null=False, primary_key=True, auto_created=True)
    name = models.CharField(max_length=100, null=False)
    price = models.IntegerField(default=0, null=True, blank=True)
    currency = models.CharField(max_length=10, null=True, default='USD', blank=True)
    category_list = models.ArrayReferenceField(
        to=Category,
        on_delete=models.CASCADE,
        blank=True,
    )
    objects = models.DjongoManager()

    def __str__(self):
        return self.name
