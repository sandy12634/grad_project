from rest_framework import permissions

class IsSuperAdminOrPublicReadOnly(permissions.BasePermission):
    """
    تسمح بطلبات الـ GET والـ POST للعامة (Public)،
    بينما العمليات الأخرى (تعديل، حذف) تتطلب أن يكون المستخدم superadmin.
    """
    def has_permission(self, request, view):
        # السماح للعامة بطلب استعراض البيانات (GET) أو إرسال استفسار جديد (POST)
        if request.method in permissions.SAFE_METHODS or request.method == "POST":
            return True
        
        # لأي عمليات أخرى (إن وجدت مستقبلاً كـ PUT أو DELETE)، يجب أن يكون superadmin
        return (
            request.user and 
            request.user.is_authenticated and 
            getattr(request.user, 'role', None) == "superadmin"
        )