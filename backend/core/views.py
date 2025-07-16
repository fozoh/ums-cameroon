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