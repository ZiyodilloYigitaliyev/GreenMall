from rest_framework.generics import CreateAPIView, ListAPIView
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # ✅ PDF yaratish va URL olish
        pdf_url = generate_user_pdf(user)

        # ✅ Agar PDF yaratishda muammo bo‘lsa, xabar beramiz
        if not pdf_url:
            return Response(
                {"error": "PDF yaratishda xatolik yuz berdi"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                "message": "User created successfully",
                "name": user.name,
                "surname": user.surname,
                "phone": user.phone,
                "address": user.address,
                "pdf_url": pdf_url,  # ✅ Endi `response` ichida ko‘rinadi
            },
            status=status.HTTP_201_CREATED
        )

class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = self.get_serializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)