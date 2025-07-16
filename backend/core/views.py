
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from .models import SchoolSettings
from .serializers import SchoolSettingsSerializer

# Admin API for School Settings
class SchoolSettingsView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        settings = SchoolSettings.objects.first()
        serializer = SchoolSettingsSerializer(settings)
        return Response(serializer.data)

    def post(self, request):
        settings = SchoolSettings.objects.first()
        if settings:
            serializer = SchoolSettingsSerializer(settings, data=request.data, partial=True)
        else:
            serializer = SchoolSettingsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
from .serializers import ProgramSerializer

class AdminProgramManagementView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        programs = Program.objects.all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        program = get_object_or_404(Program, pk=pk)
        serializer = ProgramSerializer(program, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        program = get_object_or_404(Program, pk=pk)
        program.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# --- Admin Management for Programs, Departments, Courses ---
from .models import Program, Department, Course
from .serializers import DepartmentSerializer, CourseSerializer

class AdminDepartmentManagementView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = DepartmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        department = get_object_or_404(Department, pk=pk)
        serializer = DepartmentSerializer(department, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        department = get_object_or_404(Department, pk=pk)
        department.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AdminCourseManagementView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        course = get_object_or_404(Course, pk=pk)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# --- Admin Portal Views ---
from rest_framework.permissions import IsAdminUser

class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)
        if user and user.role == 'admin':
            token = get_tokens_for_user(user)
            return Response({'token': token, 'user': UserSerializer(user).data})
        return Response({'error': 'Invalid admin credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class AdminUserManagementView(APIView):
    permission_classes = [IsAdminUser]
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Create new user (admin, staff, or student)
        data = request.data.copy()
        role = data.get('role', 'student')
        password = data.get('password')
        if not password:
            return Response({'error': 'Password required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.create_user(
                email=data.get('email'),
                password=password,
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                role=role
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
# Detail views for messages, events, documents, and feedback
from rest_framework.generics import RetrieveAPIView
from .models import Message, Event, DocumentUpload, Feedback
from .serializers import MessageSerializer, EventSerializer, DocumentUploadSerializer, FeedbackSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.models import Avg
class MessageDetailView(RetrieveAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class EventDetailView(RetrieveAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

class DocumentUploadDetailView(RetrieveAPIView):
    queryset = DocumentUpload.objects.all()
    serializer_class = DocumentUploadSerializer
    permission_classes = [IsAuthenticated]

class FeedbackDetailView(RetrieveAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [IsAuthenticated]
# UserList API for messaging tab
from rest_framework.generics import ListAPIView
from .models import User
from .serializers import UserSerializer

class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
# User list API view for messaging
# ...existing code...
# ...existing code...
# ...existing code...
# Department list API view
from .serializers import DepartmentSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

class DepartmentListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        from .models import Department
        departments = Department.objects.all()
        serializer = DepartmentSerializer(departments, many=True)
        return Response(serializer.data)


# Import models
from .models import (
    User, Student, Lecturer, Department, Course, EnrolledCourse,
    TranscriptRequest, Payment, Attendance, UserProfile, Notification, AuditLog
)

# Import serializers
from .serializers import (
    UserSerializer, StudentSerializer, CourseSerializer,
    EnrolledCourseSerializer, TranscriptRequestSerializer, PaymentSerializer
)


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
        try:
            student = Student.objects.get(user=request.user)
            TranscriptRequest.objects.create(student=student)
            return Response({'message': 'Transcript request submitted'})
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)


class PaymentHistoryView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            student = Student.objects.get(user=request.user)
            payments = Payment.objects.filter(student=student)
            data = [{'amount': p.amount, 'method': p.method, 'date': p.timestamp} for p in payments]
            return Response(data)
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response(UserSerializer(request.user).data)


class LecturerAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, lecturer_id):
        lecturer = get_object_or_404(Lecturer, id=lecturer_id)
        courses = Course.objects.filter(lecturer=lecturer)
        course_stats = []
        for course in courses:
            enrolled = EnrolledCourse.objects.filter(course=course)
            avg_grade = enrolled.aggregate(Avg('final_grade'))['final_grade__avg']
            attendance = Attendance.objects.filter(course=course, present=True).count()
            course_stats.append({
                'course': course.name,
                'enrolled_count': enrolled.count(),
                'average_grade': avg_grade,
                'attendance_count': attendance
            })
        return Response({'courses': course_stats})


class DepartmentAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, department_id):
        department = get_object_or_404(Department, id=department_id)
        courses = Course.objects.filter(department=department)
        return Response({'courses': courses.values()})


class SchoolAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, school_id):
        return Response({'message': 'School analytics coming soon'})


class StudentAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, student_id):
        student = get_object_or_404(Student, id=student_id)
        # Program and department
        program = student.program.name if student.program else None
        department = student.department.name if student.department else None
        # Courses and grades
        enrollments = EnrolledCourse.objects.filter(student=student)
        courses = [
            {
                'course': e.course.name,
                'code': e.course.code,
                'ca_marks': e.ca_marks,
                'exam_marks': e.exam_marks,
                'final_grade': e.final_grade
            }
            for e in enrollments
        ]
        # Notifications
        notifications = Notification.objects.filter(user=student.user).order_by('-created_at')[:10]
        notifications_data = [
            {
                'message': n.message,
                'read': n.read,
                'created_at': n.created_at
            }
            for n in notifications
        ]
        # Feedback
        feedbacks = Feedback.objects.filter(user=student.user).order_by('-created_at')[:10]
        feedback_data = [
            {
                'course': f.course.name if f.course else None,
                'feedback_en': f.feedback_en,
                'feedback_fr': f.feedback_fr,
                'rating': f.rating,
                'created_at': f.created_at
            }
            for f in feedbacks
        ]
        return Response({
            'program': program,
            'department': department,
            'courses': courses,
            'notifications': notifications_data,
            'feedback': feedback_data
        })


class StudentRegistrationView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        program_id = request.data.get('program')
        department_id = request.data.get('department')
        try:
            user = User.objects.create_user(
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                role='student'
            )
            program = None
            department = None
            if program_id:
                from .models import Program
                program = Program.objects.get(id=program_id)
            if department_id:
                from .models import Department
                department = Department.objects.get(id=department_id)
            Student.objects.create(
                user=user,
                registration_number=f"STU{user.id}",
                department=department,
                program=program,
                level=1
            )
            return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Student can update their program
class StudentProgramUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            student = Student.objects.get(user=request.user)
            program_id = request.data.get('program')
            if not program_id:
                return Response({'error': 'Program ID required'}, status=status.HTTP_400_BAD_REQUEST)
            from .models import Program
            program = Program.objects.get(id=program_id)
            student.program = program
            student.save()
            return Response({'message': 'Program updated successfully'})
        except Student.DoesNotExist:
            return Response({'error': 'Student profile not found'}, status=status.HTTP_404_NOT_FOUND)
        except Program.DoesNotExist:
            return Response({'error': 'Program not found'}, status=status.HTTP_404_NOT_FOUND)


class AttendanceListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message': 'Attendance list not implemented yet'})

    def post(self, request):
        return Response({'message': 'Attendance submitted successfully'})


class GradeAppealListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        return Response({'message': 'Grade appeal submitted'})


class MessageListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        from .models import Message
        from .serializers import MessageSerializer
        messages = Message.objects.filter(recipient=request.user) | Message.objects.filter(sender=request.user)
        messages = messages.distinct().order_by('-timestamp')
        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request):
        from .models import Message, User
        from .serializers import MessageSerializer
        data = request.data.copy()
        data['sender'] = request.user.id
        recipient_id = data.get('recipient')
        if recipient_id:
            try:
                recipient = User.objects.get(id=recipient_id)
                data['recipient'] = recipient.id
            except User.DoesNotExist:
                return Response({'error': 'Recipient not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save(sender=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DocumentUploadListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        from .models import DocumentUpload
        from .serializers import DocumentUploadSerializer
        documents = DocumentUpload.objects.all().order_by('-uploaded_at')
        serializer = DocumentUploadSerializer(documents, many=True)
        return Response(serializer.data)

    def post(self, request):
        from .models import DocumentUpload
        from .serializers import DocumentUploadSerializer
        data = request.data.copy()
        data['uploader'] = request.user.id
        serializer = DocumentUploadSerializer(data=data)
        if serializer.is_valid():
            serializer.save(uploader=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        from .models import Event
        from .serializers import EventSerializer
        events = Event.objects.all().order_by('-date')
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)

    def post(self, request):
        from .models import Event
        from .serializers import EventSerializer
        data = request.data.copy()
        data['created_by'] = request.user.id
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackListCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        from .models import Feedback
        from .serializers import FeedbackSerializer
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        return Response(serializer.data)

    def post(self, request):
        from .models import Feedback, Course
        from .serializers import FeedbackSerializer
        data = request.data.copy()
        data['user'] = request.user.id
        course_id = data.get('course')
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
                data['course'] = course.id
            except Course.DoesNotExist:
                return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = FeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message': 'Notification list not implemented yet'})


class NotificationReadView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        return Response({'message': f'Notification {pk} details'})


class AuditLogListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({'message': 'Audit log list not implemented yet'})