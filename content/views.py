from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import News, History, Service, Facility, Event
from .serializers import (
    NewsSerializer,
    HistorySerializer,
    ServiceSerializer,
    FacilitySerializer,
    EventSerializer,
)
from accounts.premissions import IsSectorAdminOrSuperAdmin

class SectorFilteredViewSet(ModelViewSet):
    """
    ViewSet تلقائي يفلتر البيانات حسب sector المستخدم
    """
    permission_classes = [IsSectorAdminOrSuperAdmin]
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # superadmin يرى كل البيانات
        if user.role == "superadmin":
            return queryset
        
        # admin يرى فقط بيانات قطاعه
        if user.role == "admin" and user.sector:
            return queryset.filter(sector=user.sector)
        
        return queryset.none()

class NewsViewSet(SectorFilteredViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class HistoryViewSet(SectorFilteredViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class ServiceViewSet(SectorFilteredViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class FacilityViewSet(SectorFilteredViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

class EventViewSet(SectorFilteredViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer