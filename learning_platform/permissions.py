from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Разрешение, позволяющее только владельцам объекта редактировать его.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class IsTeacherOrAdmin(permissions.BasePermission):
    """
    Разрешение для преподавателей и администраторов.
    """
    def has_permission(self, request, view):
        return (request.user.groups.filter(name="teachers").exists() or 
                request.user.is_staff)


class CanManageTests(permissions.BasePermission):
    """
    Разрешение для управления тестами.
    """
    def has_object_permission(self, request, view, obj):
        # Для тестов проверяем владельца урока
        if hasattr(obj, 'lesson'):
            return obj.lesson.owner == request.user
        # Для вопросов и ответов проверяем владельца теста
        if hasattr(obj, 'test'):
            return obj.test.lesson.owner == request.user
        return False


class CanTakeTest(permissions.BasePermission):
    """
    Разрешение для прохождения тестов.
    """
    def has_object_permission(self, request, view, obj):
        # Студенты могут только просматривать и проходить тесты
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name="students").exists() 