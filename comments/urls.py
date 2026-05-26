from django.urls import path
from .views import InquiryViewSet

urlpatterns = [
    
    path('comments/', InquiryViewSet.as_view(), name='create-inquiry'),
]