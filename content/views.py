from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import News, History, Service, Facility, Event
from .serializers import (
    NewsSerializer, HistorySerializer, ServiceSerializer,
    FacilitySerializer, EventSerializer,
)
from accounts.premissions import IsSectorAdminOrSuperAdmin

class SectorFilteredViewSet(ModelViewSet):
    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsSectorAdminOrSuperAdmin()]

    def get_queryset(self):
        
        queryset = self.queryset
        user = self.request.user
        
        
        if not user.is_anonymous:
            if user.role == "superadmin":
                pass 
            elif user.role == "admin" and user.sector:
                queryset = queryset.filter(sector=user.sector)
            else:
                return queryset.none()
        
        
        
        sector_filter = self.request.query_params.get('sector')
        if sector_filter:
            queryset = queryset.filter(sector=sector_filter)
            
        return queryset


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