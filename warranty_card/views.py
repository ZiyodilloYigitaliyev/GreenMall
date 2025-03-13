from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.conf import settings
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

        pdf_filename = generate_user_pdf(user)

        pdf_url = generate_user_pdf(user)
        return Response(
            {
                "message": "User created successfully",
                "pdf_url": pdf_url,
            },
            status=status.HTTP_201_CREATED
        )

