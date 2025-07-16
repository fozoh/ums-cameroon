from django.urls import path
from .views import (
    # Auth & Token
    LoginView,
    HelloView,

    # Student Portal
    MyCoursesView,
    RegisterCourseView,
    TranscriptRequestView,
    PaymentHistoryView,

    # Admin & Analytics
    DepartmentListView,
    UserProfileView,
    LecturerAnalyticsView,
    DepartmentAnalyticsView,
    SchoolAnalyticsView,
    StudentAnalyticsView,

    # Registration & Attendance
    StudentRegistrationView,
    AttendanceListCreateView,
    GradeAppealListCreateView,

    # Messaging & Notifications
    MessageListCreateView,
    DocumentUploadListCreateView,
    EventListCreateView,
    FeedbackListCreateView,
    NotificationListView,
    NotificationReadView,

    # Audit & Logs
    AuditLogListView,
    UserList,
)

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # 🔐 Authentication
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 🧪 Test API
    path('hello/', HelloView.as_view(), name='hello'),

    # 📚 Course & Student Management
    path('my-courses/', MyCoursesView.as_view(), name='my_courses'),
    path('register-course/', RegisterCourseView.as_view(), name='register_course'),
    path('transcript-request/', TranscriptRequestView.as_view(), name='transcript_request'),
    path('payment-history/', PaymentHistoryView.as_view(), name='payment_history'),
    path('departments/', DepartmentListView.as_view(), name='department_list'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('register/student/', StudentRegistrationView.as_view(), name='student-register'),
    path('attendance/', AttendanceListCreateView.as_view(), name='attendance-list-create'),

    # 📊 Analytics & Reports
    path('analytics/lecturer/<int:lecturer_id>/', LecturerAnalyticsView.as_view(), name='lecturer-analytics'),
    path('analytics/department/<int:department_id>/', DepartmentAnalyticsView.as_view(), name='department-analytics'),
    path('analytics/school/<int:school_id>/', SchoolAnalyticsView.as_view(), name='school-analytics'),
    path('analytics/student/<int:student_id>/', StudentAnalyticsView.as_view(), name='student-analytics'),

    # 💬 Messaging & Content
    path('users/', UserList.as_view(), name='user-list'),
    path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
    path('documents/', DocumentUploadListCreateView.as_view(), name='document-list-create'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),

    # 🛎️ Notifications & Audit
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/read/', NotificationReadView.as_view(), name='notification_read'),
    path('auditlog/', AuditLogListView.as_view(), name='audit_log'),
]