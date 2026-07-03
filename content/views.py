from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response



from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import News, History, Service, Facility, Event
from .serializers import (
    NewsSerializer,
    HistorySerializer,
    ServiceSerializer,
    FacilitySerializer,
    EventSerializer,
)
from accounts.premissions import IsSectorAdminOrSuperAdmin

class SectorFilteredViewSet(ModelViewSet):
    """
    ViewSet تلقائي يفلتر البيانات حسب sector المستخدم
    """
    """permission_classes = [IsSectorAdminOrSuperAdmin]"""
    
    def get_permissions(self):
        """
        تخصيص الصلاحيات: طلب الـ GET متاح للعامة بدون أدمن وبدون قطاع (Public)،
        أما باقي الطلبات فتطلب صلاحيات الأدمن والقطاع من تطبيق account.
        """
        # إذا كان الطلب GET (استعراض الأخبار)، نجعله Public تماماً دون أي شروط
        if self.request.method == 'GET':
            return [AllowAny()]
        
        # لأي عمليات أخرى كالإضافة والتعديل والحذف (POST, PUT, DELETE)
        # نطبق البيرمشن المستورد من تطبيق account
        return [IsSectorAdminOrSuperAdmin()]
    
    
    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()
        
        # superadmin يرى كل البيانات
        if user.role == "superadmin":
            return queryset
        
        # admin يرى فقط بيانات قطاعه
        if user.role == "admin" and user.sector:
            return queryset.filter(sector=user.sector)
        
        return queryset.none()

class NewsViewSet(SectorFilteredViewSet):
     queryset = News.objects.all()
   
     serializer_class = NewsSerializer

   
     def get_queryset(self):
        user = self.request.user
        
        # 1. إذا كان المستخدم غير مسجل دخول (طلب عام Public)
        if user.is_anonymous:
            return News.objects.all()
            
        # 2. فحص الـ role والـ sector للمسؤولين (الكود الحالي تبعك)
        if hasattr(user, 'role') and user.role == 'superadmin':
            return News.objects.all()
            
        if hasattr(user, 'role') and user.role == 'admin' and hasattr(user, 'sector'):
            return News.objects.filter(sector=user.sector)
            
        return News.objects.none()

    # ---- إضافة مسار الفلترة المخصص هنا ----
    # url_path='sector/(?P<sector_id>[^/.]+)' لتمرير الآي دي بالـ URL مباشرة
     @action(detail=False, methods=['get'], url_path='(?P<sector_name>[^/.]+)', permission_classes=[AllowAny])
     def by_sector(self, request, sector_name=None):
        """
        مسار مخصص للـ Public بيجيب الأخبار بناءً على اسم القطاع الممرر بالرابط
        """
        # التعديل هنا: الفلترة مباشرة على الحقل لأنه CharField وليس ForeignKey
        filtered_news = News.objects.filter(sector=sector_name)
        
        serializer = self.get_serializer(filtered_news, many=True)
        return Response(serializer.data)

class HistoryViewSet(SectorFilteredViewSet):
    queryset = History.objects.all()
    serializer_class = HistorySerializer
    def get_queryset(self):
        user = self.request.user

        # 1. إذا كان المستخدم غير مسجل دخول (طلب عام Public لـ الخدمات)
        if user.is_anonymous:
            # عديلي السطر هاد حسب كيف بدك الخدمات تظهر للعامة:
            # إذا بدك كل الخدمات تظهر للكل:
            return History.objects.all() 
            
            # أو إذا بدك بس الخدمات يلي ما بتتبع لقطاع معين:
            # return Service.objects.filter(sector__isnull=True)

        # 2. الكود الحالي تبعك (يلي بيفحص الـ role والـ sector)
        # انقليه لهون متل ما هو تماماً مشان يشتغل للأدمن بأمان
        if hasattr(user, 'role') and user.role == 'superadmin':
            return History.objects.all()
        
        
        if hasattr(user, 'role') and user.role == 'admin' and hasattr(user, 'sector'):
            return History.objects.filter(sector=user.sector)
            
        return History.objects.none()

    # ---- إضافة مسار الفلترة المخصص هنا ----
    # url_path='sector/(?P<sector_id>[^/.]+)' لتمرير الآي دي بالـ URL مباشرة
    @action(detail=False, methods=['get'], url_path='(?P<sector_name>[^/.]+)', permission_classes=[AllowAny])
    def by_sector(self, request, sector_name=None):
        """
        مسار مخصص للـ Public بيجيب الأخبار بناءً على اسم القطاع الممرر بالرابط
        """
        # التعديل هنا: الفلترة مباشرة على الحقل لأنه CharField وليس ForeignKey
        filtered_history = History.objects.filter(sector=sector_name)
        
        serializer = self.get_serializer(filtered_history, many=True)
        return Response(serializer.data)

    

class ServiceViewSet(SectorFilteredViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    def get_queryset(self):
        user = self.request.user

        # 1. إذا كان المستخدم غير مسجل دخول (طلب عام Public لـ الخدمات)
        if user.is_anonymous:
            # عديلي السطر هاد حسب كيف بدك الخدمات تظهر للعامة:
            # إذا بدك كل الخدمات تظهر للكل:
            return Service.objects.all() 
            
            # أو إذا بدك بس الخدمات يلي ما بتتبع لقطاع معين:
            # return Service.objects.filter(sector__isnull=True)

        # 2. الكود الحالي تبعك (يلي بيفحص الـ role والـ sector)
        # انقليه لهون متل ما هو تماماً مشان يشتغل للأدمن بأمان
        if hasattr(user, 'role') and user.role == 'superadmin':
            return Service.objects.all()
        
                
                
        if hasattr(user, 'role') and user.role == 'admin' and hasattr(user, 'sector'):
            return Service.objects.filter(sector=user.sector)
            
        return Service.objects.none()

    # ---- إضافة مسار الفلترة المخصص هنا ----
    # url_path='sector/(?P<sector_id>[^/.]+)' لتمرير الآي دي بالـ URL مباشرة
    @action(detail=False, methods=['get'], url_path='(?P<sector_name>[^/.]+)', permission_classes=[AllowAny])
    def by_sector(self, request, sector_name=None):
        """
        مسار مخصص للـ Public بيجيب الأخبار بناءً على اسم القطاع الممرر بالرابط
        """
        # التعديل هنا: الفلترة مباشرة على الحقل لأنه CharField وليس ForeignKey
        filtered_services = History.objects.filter(sector=sector_name)
        
        serializer = self.get_serializer(filtered_services, many=True)
        return Response(serializer.data)
    

class FacilityViewSet(SectorFilteredViewSet):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    def get_queryset(self):
        user = self.request.user

        # 1. إذا كان المستخدم غير مسجل دخول (طلب عام Public لـ الخدمات)
        if user.is_anonymous:
            # عديلي السطر هاد حسب كيف بدك الخدمات تظهر للعامة:
            # إذا بدك كل الخدمات تظهر للكل:
            return Facility.objects.all() 
            
            # أو إذا بدك بس الخدمات يلي ما بتتبع لقطاع معين:
            # return Service.objects.filter(sector__isnull=True)

        # 2. الكود الحالي تبعك (يلي بيفحص الـ role والـ sector)
        # انقليه لهون متل ما هو تماماً مشان يشتغل للأدمن بأمان
        if hasattr(user, 'role') and user.role == 'superadmin':
            return Facility.objects.all()
        
        if hasattr(user, 'role') and user.role == 'admin' and hasattr(user, 'sector'):
            return Facility.objects.filter(sector=user.sector)
            
        return Facility.objects.none()

    # ---- إضافة مسار الفلترة المخصص هنا ----
    # url_path='sector/(?P<sector_id>[^/.]+)' لتمرير الآي دي بالـ URL مباشرة
    @action(detail=False, methods=['get'], url_path='(?P<sector_name>[^/.]+)', permission_classes=[AllowAny])
    def by_sector(self, request, sector_name=None):
        """
        مسار مخصص للـ Public بيجيب الأخبار بناءً على اسم القطاع الممرر بالرابط
        """
        # التعديل هنا: الفلترة مباشرة على الحقل لأنه CharField وليس ForeignKey
        filtered_facility = Facility.objects.filter(sector=sector_name)
        
        serializer = self.get_serializer(filtered_facility, many=True)
        return Response(serializer.data)

class EventViewSet(SectorFilteredViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def get_queryset(self):
        user = self.request.user

        # 1. إذا كان المستخدم غير مسجل دخول (طلب عام Public لـ الخدمات)
        if user.is_anonymous:
           
            return Event.objects.all() 
            
            # أو إذا بدك بس الخدمات يلي ما بتتبع لقطاع معين:
            # return Service.objects.filter(sector__isnull=True)

        # 2. الكود الحالي تبعك (يلي بيفحص الـ role والـ sector)
        # انقليه لهون متل ما هو تماماً مشان يشتغل للأدمن بأمان
        if hasattr(user, 'role') and user.role == 'superadmin':
            return Event.objects.all()
        if hasattr(user, 'role') and user.role == 'admin' and hasattr(user, 'sector'):
            return Event.objects.filter(sector=user.sector)
            
        return Event.objects.none()

    # ---- إضافة مسار الفلترة المخصص هنا ----
    # url_path='sector/(?P<sector_id>[^/.]+)' لتمرير الآي دي بالـ URL مباشرة
    @action(detail=False, methods=['get'], url_path='(?P<sector_name>[^/.]+)', permission_classes=[AllowAny])
    def by_sector(self, request, sector_name=None):
        """
        مسار مخصص للـ Public بيجيب الأخبار بناءً على اسم القطاع الممرر بالرابط
        """
        # التعديل هنا: الفلترة مباشرة على الحقل لأنه CharField وليس ForeignKey
        filtered_event= Event.objects.filter(sector=sector_name)
        
        serializer = self.get_serializer(filtered_event, many=True)
        return Response(serializer.data)