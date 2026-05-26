from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Inquiry
from .serializers import InquirySerializer
from .permissions import IsSuperAdminOnly
from rest_framework import generics
from accounts.premissions import IsSectorAdminOrSuperAdmin

class InquiryViewSet(generics.ListCreateAPIView):
    serializer_class = InquirySerializer
    permission_classes = [IsSuperAdminOnly]
    
    def get_queryset(self):
        user = self.request.user
        queryset = Inquiry.objects.all().order_by("-id")
        
        # superadmin يرى كل البيانات
        if user.role == "superadmin":
            return queryset
        
        # admin يرى فقط استفسارات قطاعه
        if user.role == "admin" and user.sector:
            return queryset.filter(sector=user.sector)
        
        return queryset.none()