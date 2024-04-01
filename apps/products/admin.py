from .models import Product, Category, Shop
from django.contrib import admin
from .admins import CategoryAdmin, ShopAdmin, ProductAdmin

admin.site.register(Category, CategoryAdmin)
admin.site.register(Shop, ShopAdmin)
admin.site.register(Product, ProductAdmin)
