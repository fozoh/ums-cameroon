from django.core.management.base import BaseCommand
from core.models import User, Student, Lecturer, Department, Course, EnrolledCourse, TranscriptRequest, Payment

class Command(BaseCommand):
    help = 'Generates sample data for testing'

    def handle(self, *args, **kwargs):
        # Create Departments
        cs_dept, _ = Department.objects.get_or_create(name="Computer Science")
        ee_dept, _ = Department.objects.get_or_create(name="Electrical Engineering")



        students = []
        lecturers = []
        hods = []
        for i in range(1, 81):
            user, _ = User.objects.get_or_create(
                email=f"student{i}@example.com", role="student",
                defaults={'first_name': f'Student{i}', 'last_name': f'Lastname{i}'}
            )
            user.set_password('test1234')
            user.save()
            reg_num = f"STU{1000+i}"
            student, _ = Student.objects.get_or_create(
                registration_number=reg_num,
                defaults={
                    'user': user,
                    'department': cs_dept if i % 2 == 0 else ee_dept,
                    'level': (i % 3) + 1
                }
            )
            students.append(student)

        for i in range(1, 16):
            user, _ = User.objects.get_or_create(
                email=f"lecturer{i}@example.com", role="lecturer",
                defaults={'first_name': f'Lecturer{i}', 'last_name': f'LecLast{i}'}
            )
            user.set_password('test1234')
            user.save()
            staff_id = f"LEC{2000+i}"
            lecturer, _ = Lecturer.objects.get_or_create(
                staff_id=staff_id,
                defaults={
                    'user': user,
                    'department': cs_dept if i % 2 == 0 else ee_dept
                }
            )
            lecturers.append(lecturer)

        for i in range(1, 6):
            user, _ = User.objects.get_or_create(
                email=f"hod{i}@example.com", role="hod",
                defaults={'first_name': f'Hod{i}', 'last_name': f'HodLast{i}'}
            )
            user.set_password('test1234')
            user.save()
            staff_id = f"HOD{3000+i}"
            hod, _ = Lecturer.objects.get_or_create(
                staff_id=staff_id,
                defaults={
                    'user': user,
                    'department': cs_dept if i % 2 == 0 else ee_dept
                }
            )
            hods.append(hod)

        # Create Courses
        courses = []
        for i in range(1, 11):
            course, _ = Course.objects.get_or_create(
                code=f"CS{100+i}",
                name=f"Course {i}",
                credits=(i % 5) + 2,
                department=cs_dept if i % 2 == 0 else ee_dept,
                lecturer=lecturers[i % len(lecturers)] if lecturers else None
            )
            courses.append(course)

        # Enroll Students
        for student in students:
            for course in courses:
                if (student.id + course.id) % 3 == 0:
                    EnrolledCourse.objects.get_or_create(
                        student=student,
                        course=course,
                        semester="Sem 1",
                        ca_marks=40 + (student.id % 30),
                        exam_marks=50 + (course.id % 40)
                    )

        # Transcript Requests
        for student in students[:20]:
            TranscriptRequest.objects.get_or_create(
                student=student,
                paid=True,
                approved=True
            )

        # Payments
        for idx, student in enumerate(students[:30]):
            Payment.objects.get_or_create(
                student=student,
                amount=50000 + idx * 1000,
                reference=f"PAY{1000+idx}",
                method="MTN Mobile Money" if idx % 2 == 0 else "Orange Money"
            )

        self.stdout.write(self.style.SUCCESS('✅ Sample data created successfully'))