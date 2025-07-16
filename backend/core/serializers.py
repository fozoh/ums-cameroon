from rest_framework import serializers
from .models import (
    User, Student, Lecturer, Department, Course, EnrolledCourse,
    TranscriptRequest, Payment, UserProfile, Notification, AuditLog,
    Message, DocumentUpload, Event, Feedback, Attendance, GradeAppeal, Schedule
)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']

class LecturerSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Lecturer
        fields = ['user', 'staff_id', 'department']

class DepartmentSerializer(serializers.ModelSerializer):
    hod = LecturerSerializer()
    class Meta:
        model = Department
        fields = ['id', 'name', 'hod']

class CourseSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    lecturer = LecturerSerializer(read_only=True)
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

# Messaging Serializers
class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    recipient = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'read']

class DocumentUploadSerializer(serializers.ModelSerializer):
    uploader = UserSerializer(read_only=True)
    class Meta:
        model = DocumentUpload
        fields = ['id', 'uploader', 'title', 'file', 'uploaded_at', 'description']

class EventSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Event
        fields = ['id', 'title_en', 'title_fr', 'description_en', 'description_fr',
                  'date', 'created_by', 'created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'course', 'feedback_en', 'feedback_fr', 'rating', 'created_at']
# Minimal StudentSerializer for nested use
class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Student
        fields = ['id', 'registration_number', 'user', 'department', 'program', 'school', 'level']

class AttendanceSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'present']

class GradeAppealSerializer(serializers.ModelSerializer):
    student = StudentSerializer(read_only=True)
    course = CourseSerializer(read_only=True)
    class Meta:
        model = GradeAppeal
        fields = ['id', 'student', 'course', 'reason_en', 'reason_fr',
                  'status', 'response_en', 'response_fr', 'created_at', 'updated_at']

class ScheduleSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    program = serializers.StringRelatedField(read_only=True)
    school = serializers.StringRelatedField(read_only=True)
    lecturer = LecturerSerializer(read_only=True)
    class Meta:
        model = Schedule
        fields = ['id', 'course', 'program', 'school', 'lecturer',
                  'day_of_week', 'start_time', 'end_time', 'location_en', 'location_fr']