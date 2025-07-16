# SchoolSettings model for per-school customization
from django.db import models

class SchoolSettings(models.Model):
    name = models.CharField(max_length=255, default="University")
    logo = models.ImageField(upload_to='school_logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=20, default="#008000")  # Green
    secondary_color = models.CharField(max_length=20, default="#FFD700")  # Yellow
    accent_color = models.CharField(max_length=20, default="#FF0000")  # Red
    language = models.CharField(max_length=10, choices=[('en', 'English'), ('fr', 'French')], default='en')
    grading_scale = models.CharField(max_length=255, default="A-F")
    contact_email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
# Multilingual support
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

# School model
class School(models.Model):
    name_en = models.CharField(max_length=255)
    name_fr = models.CharField(max_length=255)
    address_en = models.CharField(max_length=255, blank=True)
    address_fr = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.name_en} / {self.name_fr}"

# Program model
class Program(models.Model):
    PROGRAM_TYPE_CHOICES = (
        ('hnd', _('HND')),
        ('degree', _('Degree')),
        ('masters', _('Masters')),
        ('phd', _('PhD')),
        ('certification', _('Certification')),
    )
    name_en = models.CharField(max_length=100)
    name_fr = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=PROGRAM_TYPE_CHOICES)
    school = models.ForeignKey('School', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name_en} / {self.name_fr} ({self.get_type_display()})"
# Audit log model
class AuditLog(models.Model):
    user = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    details = models.TextField(blank=True)

    def __str__(self):
        return f"{self.timestamp}: {self.user} {self.action} {self.model} {self.object_id}"

# Notification model
class Notification(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.email}: {self.message}"

# User profile model
class UserProfile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=255, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.email}"

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('lecturer', 'Lecturer'),
        ('hod', 'Head of Department'),
        ('dean', 'Dean of Studies'),
        ('director', 'Director'),
        ('vc', 'Vice Chancellor'),
    )

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    registration_number = models.CharField(max_length=30, unique=True, blank=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    program = models.ForeignKey('Program', on_delete=models.SET_NULL, null=True)
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True)
    level = models.IntegerField()  # Year of study

    def save(self, *args, **kwargs):
        # Auto-generate matricule if not set
        if not self.registration_number and self.department and self.school and self.user:
            dept_code = self.department.name[:3].upper() if self.department else 'XXX'
            school_code = self.school.name_en[:3].upper() if self.school else 'SCH'
            user_id = str(self.user.id).zfill(4)
            self.registration_number = f"{school_code}-{dept_code}-{user_id}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.registration_number


class Lecturer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'role': 'lecturer'})
    staff_id = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.staff_id


class Department(models.Model):
    name = models.CharField(max_length=100)
    hod = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True, related_name='hod_department')

    def __str__(self):
        return self.name


class Course(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    credits = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    lecturer = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class EnrolledCourse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.CharField(max_length=20)
    ca_marks = models.FloatField(null=True, blank=True)
    exam_marks = models.FloatField(null=True, blank=True)
    final_grade = models.CharField(max_length=2, blank=True)

    def save(self, *args, **kwargs):
        if self.ca_marks is not None and self.exam_marks is not None:
            total = self.ca_marks * 0.4 + self.exam_marks * 0.6
            if total >= 70:
                self.final_grade = 'A'
            elif total >= 60:
                self.final_grade = 'B'
            elif total >= 50:
                self.final_grade = 'C'
            else:
                self.final_grade = 'F'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.registration_number} - {self.course.name}"


class TranscriptRequest(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    approved = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    def __str__(self):
        return f"Transcript for {self.student.registration_number}"


class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=100)
    method = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment: {self.amount} by {self.student.registration_number}"

# Attendance model
class Attendance(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    date = models.DateField()
    present = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student.registration_number} - {self.course.name} - {self.date}"

# Grade Appeal model
class GradeAppeal(models.Model):
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    reason_en = models.TextField()
    reason_fr = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('reviewed', 'Reviewed'), ('resolved', 'Resolved')], default='pending')
    response_en = models.TextField(blank=True)
    response_fr = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Appeal: {self.student.registration_number} - {self.course.name} - {self.status}"

# Schedule model
class Schedule(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE)
    program = models.ForeignKey('Program', on_delete=models.CASCADE)
    school = models.ForeignKey('School', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10)
    start_time = models.TimeField()
    end_time = models.TimeField()
    location_en = models.CharField(max_length=100)
    location_fr = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.course.name} - {self.day_of_week} {self.start_time}-{self.end_time}"

# Messaging model
class Message(models.Model):
    sender = models.ForeignKey('User', on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey('User', on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"From {self.sender.email} to {self.recipient.email} at {self.timestamp}"

# Document upload model
class DocumentUpload(models.Model):
    uploader = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.uploader.email}"

# Event/Announcement model
class Event(models.Model):
    title_en = models.CharField(max_length=255)
    title_fr = models.CharField(max_length=255)
    description_en = models.TextField()
    description_fr = models.TextField(blank=True)
    date = models.DateField()
    created_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title_en} / {self.title_fr}"

# Feedback/Survey model
class Feedback(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    course = models.ForeignKey('Course', on_delete=models.SET_NULL, null=True, blank=True)
    feedback_en = models.TextField()
    feedback_fr = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.email} for {self.course.name if self.course else 'General'}"