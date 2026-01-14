from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Subject, Grade, Profile

class SchoolDiaryTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.math = Subject.objects.create(name='Mathematics')
        
    def test_registration_student(self):
        response = self.client.post(reverse('register'), {
            'username': 'student1',
            'first_name': 'Ivan',
            'last_name': 'Ivanov',
            'password': 'password123',
            'role': 'student'
        })
        self.assertEqual(response.status_code, 302) # Redirect to home
        self.assertTrue(User.objects.filter(username='student1').exists())
        user = User.objects.get(username='student1')
        self.assertEqual(user.profile.role, 'student')
        
    def test_registration_teacher(self):
        response = self.client.post(reverse('register'), {
            'username': 'teacher1',
            'first_name': 'Petr',
            'last_name': 'Petrov',
            'password': 'password123',
            'role': 'teacher'
        })
        self.assertEqual(response.status_code, 302)
        user = User.objects.get(username='teacher1')
        self.assertEqual(user.profile.role, 'teacher')

    def test_teacher_can_add_grade(self):
        # Create teacher
        teacher = User.objects.create_user(username='teacher', password='pw')
        teacher.profile.role = 'teacher'
        teacher.profile.save()
        
        # Create student
        student = User.objects.create_user(username='student', password='pw')
        # Defaults to student role via signal
        
        self.client.login(username='teacher', password='pw')
        
        response = self.client.post(reverse('add_grade'), {
            'student': student.id,
            'subject': self.math.id,
            'value': 5,
            'comment': 'Good job'
        })
        self.assertEqual(response.status_code, 302)
        
        grade = Grade.objects.first()
        self.assertEqual(grade.value, 5)
        self.assertEqual(grade.student, student)
        self.assertEqual(grade.teacher, teacher)

    def test_student_dashboard_averages(self):
        student = User.objects.create_user(username='student', password='pw')
        # Profile created by signal
        
        # Add grades
        Grade.objects.create(student=student, subject=self.math, value=5)
        Grade.objects.create(student=student, subject=self.math, value=4)
        
        self.client.login(username='student', password='pw')
        response = self.client.get(reverse('subject_list'))
        
        self.assertContains(response, 'Mathematics')
        # Average should be 4.5
        # Depending on template rendering, check context or string
        self.assertEqual(response.context['subjects'][0].average, 4.5)
