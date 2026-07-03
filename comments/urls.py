from django.db import router
from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import InquiryViewSet  # تأكدي من اسم الـ ViewSet الخاص بكِ
urlpatterns = [
# 1. إنشاء الـ Router وتسجيل الـ ViewSet
path('faq/', InquiryViewSet.as_view(), name='create-inquiry'),

path('faq/<int:pk>/', InquiryViewSet.as_view(), name='faq-detail'),
]