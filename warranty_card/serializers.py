from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "surname", "phone", "address"]

    def create(self, validated_data):
        validated_data["username"] = f"{validated_data['name']}{validated_data['surname']}".replace(" ", "").lower()
        return super().create(validated_data)
