from .views import RegisterView, LoginView
from django.urls import path
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path("register/", RegisterView.as_view(), name='register'),
    path("login/", LoginView.as_view(), name='login'),
]