from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    SchoolSettingsView,
    StudentProgramUpdateView,
    AdminProgramManagementView,
    AdminDepartmentManagementView,
    AdminCourseManagementView,
    AdminLoginView,
    AdminUserManagementView,
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

    # Detail views
    MessageDetailView,
    EventDetailView,
    DocumentUploadDetailView,
    FeedbackDetailView,
)



urlpatterns = [
    path('admin/settings/', SchoolSettingsView.as_view(), name='school-settings'),
    path('student/update-program/', StudentProgramUpdateView.as_view(), name='student-update-program'),
    path('admin/programs/', AdminProgramManagementView.as_view(), name='admin-program-management'),
    path('admin/programs/<int:pk>/', AdminProgramManagementView.as_view(), name='admin-program-detail'),
    # --- Admin Management ---
    path('admin/departments/', AdminDepartmentManagementView.as_view(), name='admin-department-management'),
    path('admin/departments/<int:pk>/', AdminDepartmentManagementView.as_view(), name='admin-department-detail'),
    path('admin/courses/', AdminCourseManagementView.as_view(), name='admin-course-management'),
    path('admin/courses/<int:pk>/', AdminCourseManagementView.as_view(), name='admin-course-detail'),
    # --- Admin Portal ---
    path('admin/login/', AdminLoginView.as_view(), name='admin-login'),
    path('admin/users/', AdminUserManagementView.as_view(), name='admin-user-management'),
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
    path('messages/<int:pk>/', MessageDetailView.as_view(), name='message-detail'),
    path('documents/', DocumentUploadListCreateView.as_view(), name='document-list-create'),
    path('documents/<int:pk>/', DocumentUploadDetailView.as_view(), name='document-detail'),
    path('events/', EventListCreateView.as_view(), name='event-list-create'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback-list-create'),
    path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback-detail'),

    # 🛎️ Notifications & Audit
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:pk>/read/', NotificationReadView.as_view(), name='notification_read'),
    path('auditlog/', AuditLogListView.as_view(), name='audit_log'),
]