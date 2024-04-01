from django.db import models
from django.contrib.postgres.fields import ArrayField
from apps.commons.models import BaseModel
from .shop import Shop
from .category import Category


class Product(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    amount = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=False)
    images = ArrayField(models.CharField(max_length=200), blank=True, default=list)

    category = models.ManyToManyField(Category, related_name='products')
    shop = models.ForeignKey(Shop, related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def orders_count(self):
        return self.orders.count()

    @orders_count.setter
    def orders_count(self, value):
        pass

    def reduce_amount(self, quantity):
        if quantity > self.amount:
            return False

        self.amount -= quantity
        self.save()
        return True

    class Meta:
        ordering = ['title']


