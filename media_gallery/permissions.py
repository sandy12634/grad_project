from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # السماح للجميع بـ GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        # السماح فقط للمدراء بالرفع/التعديل
        return request.user and request.user.is_staff