from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from .models import MonthlyStat, SectorStat
from .serializers import MonthlyStatSerializer, SectorStatSerializer

class MonthlyStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = MonthlyStat.objects.all()
    serializer_class = MonthlyStatSerializer
    permission_classes = [AllowAny]

class SectorStatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SectorStat.objects.all()
    serializer_class = SectorStatSerializer
    permission_classes = [AllowAny]