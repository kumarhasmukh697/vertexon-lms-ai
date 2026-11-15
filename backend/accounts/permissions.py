from rest_framework.permissions import BasePermission





class IsStudent(BasePermission):
    """
    Allows access only to students.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'student'
        )




class IsInstructor(BasePermission):
    """
    Allows access only to instructors.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'instructor'
        )


class IsAdmin(BasePermission):
    """
    Allows access only to admins.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role == 'admin'
                or request.user.is_superuser
            )
        )


class IsInstructorOrAdmin(BasePermission):
    """
    Allows access to instructors and admins.
    """

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.role in ['instructor', 'admin']
                or request.user.is_superuser
            )
        )




class IsCourseOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.user.is_superuser or request.user.role == 'admin':
            return True

        return obj.instructor == request.user

