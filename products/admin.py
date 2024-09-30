from django.contrib import admin
from .models import *


class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    extra = 1  # Add one extra empty form to add a new media file

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_uz', 'short_description', 'price')
    inlines = [ProductMediaInline]

    def short_description(self, obj):
        # Descriptionni 100 so'zga qisqartirish
        return ' '.join(obj.description_uz.split()[:100]) + '...' if len(obj.description_uz.split()) > 100 else obj.description_uz

    short_description.short_description = 'Description'  # Admin panelda ko'rinadigan nom


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'file')

