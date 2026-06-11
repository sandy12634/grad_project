from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MonthlyStatViewSet, SectorStatViewSet

router = DefaultRouter()
router.register("stats/monthly", MonthlyStatViewSet, basename='monthly-stats')
router.register("stats/sectors", SectorStatViewSet, basename='sector-stats')

urlpatterns = [
    path('', include(router.urls)),
]