from django.contrib import admin
from .models import Inquiry # استيراد المودل الجديد

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    # الحقول التي ستظهر في القائمة الرئيسية للجدول
    list_display = ('name', 'sector',)
    
    # إضافة خيارات الفلترة في الجانب (مفيد جداً لفرز الأسئلة حسب القطاع)
    list_filter = ('sector',)
    
    # إضافة إمكانية البحث (يمكنك البحث عن اسم الشخص أو نص السؤال)
    search_fields = ('name', 'question')
    
  