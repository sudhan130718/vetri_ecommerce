from django.contrib import admin

# Register your models here.
from .models import Category,Product, Subcategory, Brands

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Subcategory)
admin.site.register(Brands)