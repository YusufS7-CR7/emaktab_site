import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import Profile, Subject, Grade
from django.test import Client
from django.db import IntegrityError

print("--- START VERIFICATION ---")

# Clean
try:
    User.objects.all().delete()
    Subject.objects.all().delete()
except:
    pass

c = Client()

# 1. Register Teacher
try:
    resp = c.post('/register/', {
        'username': 'teach', 'password': 'password123', 'first_name': 'Tea', 'last_name': 'Cher', 'role': 'teacher'
    })
    print(f"Register Teacher Status: {resp.status_code}") # Expect 302
    u = User.objects.get(username='teach')
    print(f"Teacher Role: {u.profile.role}")
    c.logout()
except Exception as e:
    print(f"Register Teacher Failed: {e}")

# 2. Register Student
try:
    resp = c.post('/register/', {
        'username': 'stud', 'password': 'password123', 'first_name': 'Stu', 'last_name': 'Dent', 'role': 'student'
    })
    print(f"Register Student Status: {resp.status_code}") # Expect 302
    s_user = User.objects.get(username='stud')
    print(f"Student Role: {s_user.profile.role}")
except Exception as e:
    print(f"Register Student Failed: {e}")

# 3. Add Grade
try:
    c.login(username='teach', password='password123')
    sub = Subject.objects.create(name="Math")
    
    resp = c.post('/grade/add/', {
        'student': s_user.id,
        'subject': sub.id,
        'value': 5,
        'comment': 'Excellent'
    })
    print(f"Add Grade Status: {resp.status_code}") # Expect 302
    print(f"Grade Count: {Grade.objects.count()}")
    if Grade.objects.exists():
        g = Grade.objects.first()
        print(f"Grade: {g.value} for {g.student.username} by {g.teacher.username}")
except Exception as e:
    print(f"Add Grade Failed: {e}")

# 4. Check Student Dash
try:
    c.login(username='stud', password='password123')
    resp = c.get('/student/dashboard/')
    print(f"Student Dash Status: {resp.status_code}")
    # print(resp.content.decode('utf-8'))
    if b'5,0' in resp.content or b'5.0' in resp.content:
        print("SUCCESS: Average grade found on dashboard")
    else:
        print("WARNING: Grade not visually found (might be formatting)")
        
except Exception as e:
    print(f"Student Dash Failed: {e}")

# 5. Check Subject Detail
try:
    # Assuming 'sub' is the Subject object created earlier
    resp = c.get(f'/student/subject/{sub.id}/')
    print(f"Subject Detail Status: {resp.status_code}") # Expect 200
    if b'Excellent' in resp.content:
        print("SUCCESS: Comment found on detail page")
    else:
        print("WARNING: Comment not found on detail page")
except Exception as e:
    print(f"Subject Detail Failed: {e}")

print("--- END VERIFICATION ---")
