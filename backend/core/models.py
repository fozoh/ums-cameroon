from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
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
from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _

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
    registration_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True)
    level = models.IntegerField()  # Year of study

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