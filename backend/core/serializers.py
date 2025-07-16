from rest_framework import serializers
from .models import User, Student, Lecturer, Course, EnrolledCourse, TranscriptRequest, Payment, UserProfile, Notification, AuditLog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Student
        fields = ['user', 'registration_number', 'department', 'level']


class LecturerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Lecturer
        fields = ['user', 'staff_id', 'department']


# DepartmentSerializer to include hod as nested LecturerSerializer
from .models import Department

class DepartmentSerializer(serializers.ModelSerializer):
    hod = LecturerSerializer()
    class Meta:
        model = Department
        fields = ['id', 'name', 'hod']

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'code', 'name', 'credits', 'department', 'lecturer']

class EnrolledCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer()
    class Meta:
        model = EnrolledCourse
        fields = ['course', 'semester', 'ca_marks', 'exam_marks', 'final_grade']

class TranscriptRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TranscriptRequest
        fields = ['student', 'request_date', 'paid', 'approved', 'delivered']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['student', 'amount', 'reference', 'method', 'timestamp']

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone', 'address', 'avatar']

class NotificationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Notification
        fields = ['id', 'user', 'message', 'read', 'created_at']

class AuditLogSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = AuditLog
        fields = ['id', 'user', 'action', 'model', 'object_id', 'timestamp', 'details']