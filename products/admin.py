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
        words = obj.description_uz.split()
        return ' '.join(words[:100]) + ('...' if len(words) > 100 else '')

    short_description.short_description = 'Description'


@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'file_url')



