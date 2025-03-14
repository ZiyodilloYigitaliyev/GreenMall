from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from .pdf_generator import generate_user_pdf

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        # ✅ PDF yaratish
        pdf_url = generate_user_pdf(user)
        response_data = {
            "message": "User created successfully",
            "name": user.name,
            "surname": user.surname,
            "phone": user.phone,
            "address": user.address,
            "pdf_url": pdf_url,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
