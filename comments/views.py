from rest_framework import viewsets, filters
from .models import Inquiry
from .serializers import InquirySerializer
from content.views import SectorFilteredViewSet # استيراد الكلاس الأب

class InquiryViewSet(SectorFilteredViewSet): # نربطه مع الأب لنأخذ الصلاحيات وفلترة القطاع
    queryset = Inquiry.objects.all().order_by("-id")
    serializer_class = InquirySerializer
    
    
    
    def get_queryset(self):
        queryset = super().get_queryset() # يطبق فلترة القطاع أولاً
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status) # استبدل status باسم الحقل الصحيح في الموديل
        return queryset