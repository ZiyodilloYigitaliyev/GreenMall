from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from .pdf_generator import generate_user_pdf
from django.conf import settings
from rest_framework import status
from django.core.files.storage import default_storage
import os

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        # ✅ PDF yaratish
        pdf_filename = generate_user_pdf(user)

        # ✅ Fayl mavjudligini tekshiramiz
        pdf_url = f"{settings.MEDIA_URL}{pdf_filename}"
        full_pdf_path = os.path.join(settings.MEDIA_ROOT, pdf_filename)
        if not default_storage.exists(full_pdf_path):
            return Response({"error": "PDF yaratilmadi!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                "message": "User created successfully",
                "pdf_url": pdf_url,  # ✅ To‘g‘ri URL
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(username=email, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({"access": str(refresh.access_token), "refresh": str(refresh)})
        return Response({"error": "Invalid credentials"}, status=400)
