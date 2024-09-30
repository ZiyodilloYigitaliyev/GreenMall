from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.authentication import TokenAuthentication
from .models import *
from .serializers import *

class StatsListView(generics.ListAPIView):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]  # GET so'rovlari uchun ruxsat berish
        return [IsAuthenticated()]


# Custom permission class
class AllowAnyGetAuthenticatedOther(IsAuthenticated):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return super().has_permission(request, view)


class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [TokenAuthentication]

    # GET uchun ruxsat, PUT/DELETE uchun token talab qilinadi
    def get_permissions(self):
        if self.request.method == 'POST':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()