from django.contrib import admin
from .models import Inquiry # استيراد المودل الجديد

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    # الحقول التي ستظهر في القائمة الرئيسية للجدول
    list_display = ('name', 'sector', 'created_at')
    
    # إضافة خيارات الفلترة في الجانب (مفيد جداً لفرز الأسئلة حسب القطاع)
    list_filter = ('sector', 'created_at')
    
    # إضافة إمكانية البحث (يمكنك البحث عن اسم الشخص أو نص السؤال)
    search_fields = ('name', 'question')
    
    # جعل الحقول للقراءة فقط لكي لا يقوم الأدمن بتعديل سؤال المستخدم
    readonly_fields = ('created_at',)