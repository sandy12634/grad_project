from django.urls import path
from .views import InquiryViewSet

urlpatterns = [
    
    path('faq/', InquiryViewSet.as_view(), name='create-inquiry'),
    
]