from rest_framework.permissions import BasePermission, SAFE_METHODS, IsAuthenticated


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            if obj.status == 'DRAFT':
                return request.user == obj.creator
            return True
        return request.user == obj.creator or request.user.is_staff


class AddFavoritesOrOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user != obj.creator