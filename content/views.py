from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from .models import News, History, Service, Facility, Event
from .serializers import (
    NewsSerializer,
    HistorySerializer,
    ServiceSerializer,
    FacilitySerializer,
    EventSerializer,
)

class NewsViewSet(ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class HistoryViewSet(ModelViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer

class ServiceViewSet(ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class FacilityViewSet(ModelViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer