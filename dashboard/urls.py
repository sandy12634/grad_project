from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MonthlyStatViewSet, SectorStatViewSet, 
   
)
from content.views import(
     NewsViewSet, HistoryViewSet, ServiceViewSet, 
    FacilityViewSet, EventViewSet
)

router = DefaultRouter()


router.register("stats/monthly", MonthlyStatViewSet, basename='monthly-stats')
router.register("stats/sectors", SectorStatViewSet, basename='sector-stats')


router.register('news', NewsViewSet)
router.register('history', HistoryViewSet)
router.register('services', ServiceViewSet)
router.register('facilities', FacilityViewSet)
router.register('events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]