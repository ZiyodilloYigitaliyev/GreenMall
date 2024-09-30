from rest_framework import serializers
from .models import *

class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stats
        fields = ['years_in_market', 'satisfied_clients', 'installed_items_km', 'work_all_days']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'