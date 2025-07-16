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
]