from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from .pdf_generator import generate_user_pdf
from django.conf import settings
from rest_framework import status

class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        pdf_path = generate_user_pdf(user)
        user.pdf_path = pdf_path  
        user.save()
        return Response(
            {
                "message": "User registered successfully",
                "pdf_url": f"{settings.MEDIA_URL}{user.unique_code}.pdf",
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
