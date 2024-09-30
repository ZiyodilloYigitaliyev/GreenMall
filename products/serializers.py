from rest_framework import serializers
from .models import *

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductMedia
        fields = ['id', 'file']


class ProductSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Product
        fields = ['id', 'title_en', 'title_ru', 'title_uz', 'description_en', 'description_ru', 'description_uz','price', 'media', 'created_at']
