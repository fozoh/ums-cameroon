from django.core.management.base import BaseCommand
from core.models import User, Student, Lecturer, Department, Course, EnrolledCourse, TranscriptRequest, Payment

class Command(BaseCommand):
    help = 'Generates sample data for testing'

    def handle(self, *args, **kwargs):
        # Create Departments
        cs_dept, _ = Department.objects.get_or_create(name="Computer Science")
        ee_dept, _ = Department.objects.get_or_create(name="Electrical Engineering")


        # Create Users
        student_user, _ = User.objects.get_or_create(email="student1@example.com", role="student", defaults={'first_name': 'John', 'last_name': 'Doe'})
        lecturer_user, _ = User.objects.get_or_create(email="lecturer1@example.com", role="lecturer", defaults={'first_name': 'Jane', 'last_name': 'Smith'})
        hod_user, _ = User.objects.get_or_create(email="hod1@example.com", role="hod", defaults={'first_name': 'Robert', 'last_name': 'Brown'})

        # Set default password for all users
        for user in [student_user, lecturer_user, hod_user]:
            user.set_password('test1234')
            user.save()

        # Create Students
        student1, _ = Student.objects.get_or_create(
            user=student_user,
            registration_number="STU1001",
            department=cs_dept,
            level=2
        )

        # Create Lecturer
        lecturer1, _ = Lecturer.objects.get_or_create(
            user=lecturer_user,
            staff_id="LEC2001",
            department=cs_dept
        )

        hod1, _ = Lecturer.objects.get_or_create(
            user=hod_user,
            staff_id="LEC2009",
            department=cs_dept
        )

        # Create Courses
        course1, _ = Course.objects.get_or_create(
            code="CS101",
            name="Introduction to Programming",
            credits=3,
            department=cs_dept,
            lecturer=lecturer1
        )

        course2, _ = Course.objects.get_or_create(
            code="CS202",
            name="Data Structures",
            credits=4,
            department=cs_dept,
            lecturer=lecturer1
        )

        # Enroll Students
        EnrolledCourse.objects.get_or_create(
            student=student1,
            course=course1,
            semester="Sem 1",
            ca_marks=60,
            exam_marks=70
        )

        EnrolledCourse.objects.get_or_create(
            student=student1,
            course=course2,
            semester="Sem 1",
            ca_marks=45,
            exam_marks=55
        )

        # Transcript Requests
        TranscriptRequest.objects.get_or_create(
            student=student1,
            paid=True,
            approved=True
        )

        # Payments
        Payment.objects.get_or_create(
            student=student1,
            amount=50000,
            reference="PAY1001",
            method="MTN Mobile Money"
        )

        self.stdout.write(self.style.SUCCESS('✅ Sample data created successfully'))