from django.contrib import admin
from .models import *

@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ['years_in_market', 'satisfied_clients', 'installed_items_km', 'work_all_days']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'product_length', 'product_width', 'product_area')

