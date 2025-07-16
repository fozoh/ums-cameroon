from .models import Lecturer, Department, School, Course

class LecturerAnalyticsView(APIView):
    def get(self, request, lecturer_id):
        try:
            lecturer = Lecturer.objects.get(id=lecturer_id)
        except Lecturer.DoesNotExist:
            return Response({'error': 'Lecturer not found'}, status=404)

        courses = Course.objects.filter(lecturer=lecturer)
        course_stats = []
        for course in courses:
            enrolled = EnrolledCourse.objects.filter(course=course)
            avg_grade = enrolled.aggregate(models.Avg('final_grade'))['final_grade__avg']
            attendance = Attendance.objects.filter(course=course, present=True).count()
            total_attendance = Attendance.objects.filter(course=course).count()
            attendance_rate = (attendance / total_attendance * 100) if total_attendance > 0 else 0
            course_stats.append({
                'course': course.name,
                'avg_grade': avg_grade,
                'attendance_rate': attendance_rate,
                'students': enrolled.count()
            })
        return Response({'courses': course_stats})

class DepartmentAnalyticsView(APIView):
    def get(self, request, department_id):
        try:
            department = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            return Response({'error': 'Department not found'}, status=404)

        students = Student.objects.filter(department=department)
        lecturers = Lecturer.objects.filter(department=department)
        courses = Course.objects.filter(department=department)
        stats = {
            'student_count': students.count(),
            'lecturer_count': lecturers.count(),
            'course_count': courses.count()
        }
        return Response(stats)

class SchoolAnalyticsView(APIView):
    def get(self, request, school_id):
        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            return Response({'error': 'School not found'}, status=404)

        programs = Program.objects.filter(school=school)
        departments = Department.objects.filter(hod__department__school=school)
        students = Student.objects.filter(school=school)
        stats = {
            'program_count': programs.count(),
            'department_count': departments.count(),
            'student_count': students.count()
        }
        return Response(stats)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Student, EnrolledCourse, Attendance, Payment, Feedback

class StudentAnalyticsView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            return Response({'error': 'Student not found'}, status=404)

        # Grades
        courses = EnrolledCourse.objects.filter(student=student)
        grades = [
            {
                'course': ec.course.name,
                'ca_marks': ec.ca_marks,
                'exam_marks': ec.exam_marks,
                'final_grade': ec.final_grade
            } for ec in courses
        ]

        # Attendance
        attendance_records = Attendance.objects.filter(student=student)
        total_classes = attendance_records.count()
        attended = attendance_records.filter(present=True).count()
        attendance_rate = (attended / total_classes * 100) if total_classes > 0 else 0

        # Payments
        payments = Payment.objects.filter(student=student)
        payment_history = [
            {
                'amount': p.amount,
                'method': p.method,
                'timestamp': p.timestamp
            } for p in payments
        ]

        # Feedback
        feedbacks = Feedback.objects.filter(user=student.user)
        feedback_summary = [
            {
                'course': f.course.name if f.course else 'General',
                'rating': f.rating,
                'feedback_en': f.feedback_en,
                'feedback_fr': f.feedback_fr
            } for f in feedbacks
        ]

        return Response({
            'grades': grades,
            'attendance_rate': attendance_rate,
            'payment_history': payment_history,
            'feedback_summary': feedback_summary
        })
from .serializers import MessageSerializer, DocumentUploadSerializer, EventSerializer, FeedbackSerializer
from .models import Message, DocumentUpload, Event, Feedback

# Messaging API
from rest_framework import generics
class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

# Document Upload API
class DocumentUploadListCreateView(generics.ListCreateAPIView):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer

# Event API
class EventListCreateView(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

# Feedback API
class FeedbackListCreateView(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
from .serializers import AttendanceSerializer, GradeAppealSerializer, ScheduleSerializer
from .models import Attendance, GradeAppeal, Schedule
from rest_framework import generics

# Attendance API
class AttendanceListCreateView(generics.ListCreateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

# Grade Appeal API
class GradeAppealListCreateView(generics.ListCreateAPIView):
    queryset = GradeAppeal.objects.all()
    serializer_class = GradeAppealSerializer

# Schedule API
class ScheduleListView(generics.ListAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.translation import gettext as _
from .models import User, Student, Department, Program, School
from .serializers import StudentSerializer

class StudentRegistrationView(APIView):
    def post(self, request):
        data = request.data.copy()
        # Create user first
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if not all([email, password, first_name, last_name]):
            return Response({'detail': _('Missing required fields.')}, status=status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(email=email, password=password, first_name=first_name, last_name=last_name, role='student')
        data['user_id'] = user.id
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            student = serializer.save()
            return Response({
                'detail': _('Registration successful.'),
                'registration_number': student.registration_number
            }, status=status.HTTP_201_CREATED)
        else:
            user.delete()
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, generics
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import (
    Student,
    EnrolledCourse,
    TranscriptRequest,
    Payment,
    Department,
    UserProfile,
    Notification,
    AuditLog
)
from .serializers import (
    UserSerializer,
    StudentSerializer,
    CourseSerializer,
    EnrolledCourseSerializer,
    TranscriptRequestSerializer,
    PaymentSerializer,
    DepartmentSerializer,
    UserProfileSerializer,
    NotificationSerializer,
    AuditLogSerializer
)


# Department list API view
from rest_framework.views import APIView
from rest_framework.response import Response

class DepartmentListView(APIView):
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user:
            token = get_tokens_for_user(user)
            return Response({'token': token, 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class HelloView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message': 'Hello, authenticated user!'})

class MyCoursesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        if request.user.role != 'student':
            return Response({'error': 'Only students allowed'}, status=status.HTTP_403_FORBIDDEN)
        try:
            student = Student.objects.get(user=request.user)
            enrollments = EnrolledCourse.objects.filter(student=student)
            data = [{
                'course': e.course.name,
                'ca_marks': e.ca_marks,
                'exam_marks': e.exam_marks,
                'final_grade': e.final_grade
            } for e in enrollments]
            return Response(data)
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)

class RegisterCourseView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        course_id = request.data.get('course_id')
        semester = request.data.get('semester')
        try:
            course = Course.objects.get(id=course_id)
            student = Student.objects.get(user=request.user)
            EnrolledCourse.objects.create(
                student=student,
                course=course,
                semester=semester
            )
            return Response({'message': 'Course registered successfully'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class TranscriptRequestView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        student = Student.objects.get(user=request.user)
        TranscriptRequest.objects.create(student=student)
        return Response({'message': 'Transcript request submitted'})

class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        student = Student.objects.get(user=request.user)
        payments = Payment.objects.filter(student=student)
        data = [{'amount': p.amount, 'method': p.method, 'date': p.timestamp} for p in payments]
        return Response(data)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    def put(self, request):
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, user=request.user)
        notification.read = True
        notification.save()
        return Response({'status': 'read'})

class AuditLogListView(generics.ListAPIView):
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return AuditLog.objects.all().order_by('-timestamp')
        return AuditLog.objects.filter(user=user).order_by('-timestamp')