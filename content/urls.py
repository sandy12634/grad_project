from rest_framework import routers 
from django.urls import path , include 
from .views import (
    NewsViewSet,
    HistoryViewSet,
    ServiceViewSet,
    FacilityViewSet,
    EventViewSet,
)

router = routers.DefaultRouter()
router.register("news", NewsViewSet)
router.register("history", HistoryViewSet)
router.register("services", ServiceViewSet)
router.register("facilities", FacilityViewSet)
router.register("events", EventViewSet)

urlpatterns = [
    path ('',include(router.urls)),
]