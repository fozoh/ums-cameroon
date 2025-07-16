from .models import Message, DocumentUpload, Event, Feedback

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'sender', 'recipient', 'content', 'timestamp', 'read']

class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentUpload
        fields = ['id', 'uploader', 'title', 'file', 'uploaded_at', 'description']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title_en', 'title_fr', 'description_en', 'description_fr', 'date', 'created_by', 'created_at']

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'user', 'course', 'feedback_en', 'feedback_fr', 'rating', 'created_at']
from .models import Attendance, GradeAppeal, Schedule

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'course', 'date', 'present']

class GradeAppealSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeAppeal
        fields = ['id', 'student', 'course', 'reason_en', 'reason_fr', 'status', 'response_en', 'response_fr', 'created_at', 'updated_at']

class ScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'course', 'program', 'school', 'lecturer', 'day_of_week', 'start_time', 'end_time', 'location_en', 'location_fr']
from rest_framework import serializers
from .models import School, Program, Student

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['id', 'name_en', 'name_fr', 'address_en', 'address_fr']

class ProgramSerializer(serializers.ModelSerializer):
    school = SchoolSerializer(read_only=True)
    school_id = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), source='school', write_only=True)
    class Meta:
        model = Program
        fields = ['id', 'name_en', 'name_fr', 'type', 'school', 'school_id']

class StudentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    department_id = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), source='department', write_only=True)
    program_id = serializers.PrimaryKeyRelatedField(queryset=Program.objects.all(), source='program', write_only=True)
    school_id = serializers.PrimaryKeyRelatedField(queryset=School.objects.all(), source='school', write_only=True)
    class Meta:
        model = Student
        fields = ['id', 'user_id', 'registration_number', 'department_id', 'program_id', 'school_id', 'level']
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