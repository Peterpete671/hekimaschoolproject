from rest_framework import permissions

class IsAdminTeacher(permissions.BasePermission):
    """
    Allows access only to teacher admins
    """
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, 'is_admin_teacher', False))
    
class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Teachers (is_teacher) or admins can write; others read-only.
    """
    def has_permission(self, request, view):
        user = request.user
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(user and user.is_authenticated and (getattr(user,'is_teacher',False)) or (getattr(user,'is_admin_teacher',False)))
    