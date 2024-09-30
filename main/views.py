from rest_framework import generics
from .models import Stats
from .serializers import StatsSerializer

class StatsListView(generics.ListAPIView):
    queryset = Stats.objects.all()
    serializer_class = StatsSerializer
