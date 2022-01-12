from rest_framework import permissions

from forum.models import CommunityUsers


class IsCommunityAdminPermission(permissions.BasePermission):
    """
    只有社区管理员才能更新，删除成员
    """
    def has_object_permission(self, request, view, obj):
        if request.method not in ["PUT", "PATCH", "DELETE"]:
            return True
        user = CommunityUsers.objects.filter(user=request.user).first()
        if not user:
            return False
        return user.is_admin == True
