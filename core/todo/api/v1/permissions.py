from rest_framework import permissions


# prevent user to read and edit others users
class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.profile.user == request.user
