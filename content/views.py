from django.shortcuts import render
from rest_framework.permissions import AllowAny


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

        # 1. إذا كان المستخدم غير مسجل دخول (طلب عام Public لـ الخدمات)
        if user.is_anonymous:
            # عديلي السطر هاد حسب كيف بدك الخدمات تظهر للعامة:
            # إذا بدك كل الخدمات تظهر للكل:
            return News.objects.all() 
            
            # أو إذا بدك بس الخدمات يلي ما بتتبع لقطاع معين:
            # return Service.objects.filter(sector__isnull=True)

        # 2. الكود الحالي تبعك (يلي بيفحص الـ role والـ sector)
        # انقليه لهون متل ما هو تماماً مشان يشتغل للأدمن بأمان
        if hasattr(user, 'role') and user.role == 'superadmin':
            return News.objects.all()

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

class EventViewSet(SectorFilteredViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def get_queryset(self):
        user = self.request.user

        # 1. إذا كان المستخدم غير مسجل دخول (طلب عام Public لـ الخدمات)
        if user.is_anonymous:
            # عديلي السطر هاد حسب كيف بدك الخدمات تظهر للعامة:
            # إذا بدك كل الخدمات تظهر للكل:
            return Event.objects.all() 
            
            # أو إذا بدك بس الخدمات يلي ما بتتبع لقطاع معين:
            # return Service.objects.filter(sector__isnull=True)

        # 2. الكود الحالي تبعك (يلي بيفحص الـ role والـ sector)
        # انقليه لهون متل ما هو تماماً مشان يشتغل للأدمن بأمان
        if hasattr(user, 'role') and user.role == 'superadmin':
            return Event.objects.all()