from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import InquiryViewSet

router = DefaultRouter()
router.register('faqs', InquiryViewSet, basename='inquiry')

urlpatterns = [
    path('', include(router.urls)),
]