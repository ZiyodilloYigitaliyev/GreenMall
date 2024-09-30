from rest_framework import serializers
from .models import *

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMedia
        fields = ['id', 'file']


class ProjectSerializer(serializers.ModelSerializer):
    media = MediaSerializer(many=True, read_only=True)  # Nested serializer

    class Meta:
        model = Project
        fields = ['id', 'title_en', 'title_ru', 'title_uz', 'description_en', 'description_ru', 'description_uz', 'media', 'created_at']
