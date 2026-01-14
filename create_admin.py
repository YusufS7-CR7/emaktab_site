import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
password = 'admin123'
email = 'admin@example.com'

try:
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.save()
        print(f"User '{username}' updated. Password set to '{password}'.")
    else:
        User.objects.create_superuser(username, email, password)
        print(f"User '{username}' created. Password set to '{password}'.")
except Exception as e:
    print(f"Error: {e}")
