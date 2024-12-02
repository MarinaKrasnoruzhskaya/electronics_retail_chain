from rest_framework import permissions


class IsActiveUser(permissions.BasePermission):
    """ Класс для определения является ли текущий пользователь активным """

    def has_object_permission(self, request, view, obj):
        """ Метод для проверки является ли авторизованный пользователь владельцем """

        return request.user.is_active
