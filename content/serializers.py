from rest_framework import serializers
from .models import News, Service, History, Facility, Event

# Serializer للخدمات - Service
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        # الحقول مطابقة لـ export type Service
        fields = [
            'id', 'title_ar', 'title_en', 
            'description_ar', 'description_en', 
            'sector', 'cost'
        ]

# Serializer للأخبار - News
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        # الحقول مطابقة لـ export type News
        fields = [
            'id', 'title_ar', 'title_en', 
            'description_ar', 'description_en', 
            'sector', 'date', 'image'
        ]

# Serializer للتاريخ - History
class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        # الحقول مطابقة لـ export type History
        fields = [
            'id', 'title_ar', 'title_en', 
            'description_ar', 'description_en', 
            'sector', 'image'
        ]

# Serializer للفعاليات - Event
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        # الحقول مطابقة لـ export type Event
        fields = [
            'id', 'title_ar', 'title_en', 
            'description_ar', 'description_en', 
            'sector', 'date', 'image'
        ]

# Serializer للمرافق - Facility
class FacilitySerializer(serializers.ModelSerializer):
    # هنا قمنا بتعريف حقل مخصص لتجميع بيانات الموقع في كائن واحد
    location = serializers.SerializerMethodField()

    class Meta:
        model = Facility
        fields = [
            'id', 'title_ar', 'title_en', 
            'description_ar', 'description_en', 
            'sector', 'image', 'location'
        ]

    # هذه الدالة تقوم بتشكيل كائن الـ location ليطابق الـ Frontend
    def get_location(self, obj):
        return {
            "lat": obj.lat,
            "lng": obj.lng,
            "address_ar": obj.address_ar,
            "address_en": obj.address_en
        }