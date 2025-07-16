from .views import LecturerAnalyticsView, DepartmentAnalyticsView, SchoolAnalyticsView
    path('analytics/lecturer/<int:lecturer_id>/', LecturerAnalyticsView.as_view(), name='lecturer-analytics'),
    path('analytics/department/<int:department_id>/', DepartmentAnalyticsView.as_view(), name='department-analytics'),
    path('analytics/school/<int:school_id>/', SchoolAnalyticsView.as_view(), name='school-analytics'),
from .views import StudentAnalyticsView
    path('analytics/student/<int:student_id>/', StudentAnalyticsView.as_view(), name='student-analytics'),
from .views import MessageListCreateView, DocumentUploadListCreateView, EventListCreateView, FeedbackListCreateView
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('documents/', DocumentUploadListCreateView.as_view(), name='document-list-create'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
from django.urls import path
from .views import (
    LoginView,
    HelloView,
    MyCoursesView,
    RegisterCourseView,
    TranscriptRequestView,
    PaymentHistoryView,
    DepartmentListView,
    UserProfileView,
    NotificationListView,
    NotificationReadView,
    AuditLogListView
)
from .views import StudentRegistrationView, AttendanceListCreateView, GradeAppealListCreateView, ScheduleListView
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('grade-appeal/', GradeAppealListCreateView.as_view(), name='grade-appeal-list-create'),
    path('schedule/', ScheduleListView.as_view(), name='schedule-list'),
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('hello/', HelloView.as_view(), name='hello'),
    path('my-courses/', MyCoursesView.as_view(), name='my_courses'),
    path('register-course/', RegisterCourseView.as_view(), name='register_course'),
    path('transcript-request/', TranscriptRequestView.as_view(), name='transcript_request'),
    path('payment-history/', PaymentHistoryView.as_view(), name='payment_history'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/read/', NotificationReadView.as_view(), name='notification_read'),
    path('auditlog/', AuditLogListView.as_view(), name='audit_log'),
    path('register/student/', StudentRegistrationView.as_view(), name='student-register'),
]