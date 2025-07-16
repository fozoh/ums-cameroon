from rest_framework import permissions

class IsStudent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'student'

class IsLecturer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'lecturer'

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['director', 'vc', 'hod', 'dean']