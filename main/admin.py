from django.contrib import admin
from .models import Stats

@admin.register(Stats)
class StatsAdmin(admin.ModelAdmin):
    list_display = ['years_in_market', 'satisfied_clients', 'installed_items_km', 'work_all_days']
