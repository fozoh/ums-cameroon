from .models import Message, DocumentUpload, Event, Feedback

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'timestamp', 'read')

@admin.register(DocumentUpload)
class DocumentUploadAdmin(admin.ModelAdmin):
    list_display = ('uploader', 'title', 'uploaded_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title_en', 'title_fr', 'date', 'created_by', 'created_at')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
from .models import Attendance, GradeAppeal, Schedule

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'date', 'present')

@admin.register(GradeAppeal)
class GradeAppealAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'status', 'created_at', 'updated_at')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('course', 'program', 'school', 'lecturer', 'day_of_week', 'start_time', 'end_time', 'location_en', 'location_fr')
from .models import School, Program

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fr', 'address_en', 'address_fr')

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name_en', 'name_fr', 'type', 'school')
from django.contrib import admin
from .models import AuditLog, Notification, UserProfile

# AuditLog admin
@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'user', 'action', 'model', 'object_id', 'details')
    list_filter = ('action', 'model', 'user')
    search_fields = ('details', 'object_id', 'user__email')

# Notification admin
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'read', 'created_at')
    list_filter = ('read', 'created_at')
    search_fields = ('message', 'user__email')

# UserProfile admin
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'avatar')
    search_fields = ('user__email', 'phone', 'address')
from django.contrib import admin
from .models import User, Student, Lecturer, Department, Course, EnrolledCourse, TranscriptRequest, Payment

class StudentInline(admin.StackedInline):
    model = Student
    extra = 0
    can_delete = True

class LecturerInline(admin.StackedInline):
    model = Lecturer
    extra = 0
    can_delete = True

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    inlines = [StudentInline, LecturerInline]
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('date_joined',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )

# Custom Student admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registration_number', 'user', 'department', 'level')
    list_filter = ('department', 'level')
    search_fields = ('registration_number', 'user__first_name', 'user__last_name')

# Custom Lecturer admin
@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
    search_fields = ['staff_id', 'user__first_name', 'user__last_name']
    list_display = ('staff_id', 'user', 'department')
    list_filter = ('department',)

# Department admin
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    autocomplete_fields = ['hod']
    list_display = ('name', 'hod')
    search_fields = ('name',)

# Course admin
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'credits', 'department', 'lecturer')
    list_filter = ('department', 'lecturer')
    search_fields = ('code', 'name')

# EnrolledCourse admin
@admin.register(EnrolledCourse)
class EnrolledCourseAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'semester', 'ca_marks', 'exam_marks', 'final_grade')
    list_filter = ('semester', 'final_grade')
    search_fields = ('student__registration_number', 'course__name')

# TranscriptRequest admin
@admin.register(TranscriptRequest)
class TranscriptRequestAdmin(admin.ModelAdmin):
    list_display = ('student', 'request_date', 'paid', 'approved', 'delivered')
    list_filter = ('paid', 'approved', 'delivered')
    search_fields = ('student__registration_number',)
    actions = ['mark_approved', 'mark_delivered']

    def mark_approved(self, request, queryset):
        updated = queryset.update(approved=True)
        self.message_user(request, f"{updated} transcript requests marked as approved.")
    mark_approved.short_description = "Mark selected requests as approved"

    def mark_delivered(self, request, queryset):
        updated = queryset.update(delivered=True)
        self.message_user(request, f"{updated} transcript requests marked as delivered.")
    mark_delivered.short_description = "Mark selected requests as delivered"

# Payment admin
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('student', 'amount', 'reference', 'method', 'timestamp')
    list_filter = ('method',)
    search_fields = ('student__registration_number', 'reference')
    actions = ['refund_payment']

    def refund_payment(self, request, queryset):
        self.message_user(request, f"{queryset.count()} payments marked as refunded (demo action).")
    refund_payment.short_description = "Mark selected payments as refunded (demo)"