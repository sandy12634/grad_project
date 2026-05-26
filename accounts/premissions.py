from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    """
    يسمح فقط للـ superadmin
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role == "superadmin"
        )


class IsAdminOrSuperAdmin(permissions.BasePermission):
    """
    يسمح للـ admin والـ superadmin
    """
    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ["admin", "superadmin"]
        )


class IsSectorAdminOrSuperAdmin(permissions.BasePermission):
    """
    - الـ superadmin عنده وصول كامل.
    - الـ admin فقط ضمن نفس القطاع.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.role in ["admin", "superadmin"]
        )

    def has_object_permission(self, request, view, obj):

        # superadmin يعمل أي شيء
        if request.user.role == "superadmin":
            return True

        # admin فقط ضمن نفس القطاع
        return obj.sector == request.user.sector