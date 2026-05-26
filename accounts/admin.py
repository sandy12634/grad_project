from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # الحقول التي تظهر في قائمة المستخدمين
    list_display = ('username', 'email', 'role', 'sector', 'is_staff')
    
    # الحقول التي تظهر عند تعديل مستخدم (نضيف حقولنا المخصصة)
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('role', 'sector')}),
    )
    
    # الحقول التي تظهر عند إنشاء مستخدم جديد
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Custom Fields', {'fields': ('role', 'sector')}),
    )

# تسجيل المودل الجديد في لوحة التحكم
admin.site.register(User, CustomUserAdmin)