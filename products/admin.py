from django.contrib import admin
from .models import *

class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1  # Add one extra empty form to add a new media file

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_uz', 'description_uz', 'price')
    inlines = [ProductMediaInline]

@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'file')

