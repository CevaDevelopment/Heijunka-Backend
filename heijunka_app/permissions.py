from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminUser(permissions.BasePermission):
    """
        Permiso que permite solo a los usuarios con el rol 'admin' realizar acciones.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        # Solo admin puede modificar
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user and request.user.is_staff
        return True