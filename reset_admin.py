import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.auth.models import User
from app.models import Profile

username = 'admin'
password = 'admin123'

try:
    if User.objects.filter(username=username).exists():
        u = User.objects.get(username=username)
        u.set_password(password)
        u.is_superuser = True
        u.is_staff = True
        u.is_active = True
        u.save()
        print(f"User '{username}' UPDATED. Password set to '{password}'.")
    else:
        u = User.objects.create_superuser(username, 'admin@example.com', password)
        print(f"User '{username}' CREATED. Password set to '{password}'.")

    # Ensure Profile exists
    if not hasattr(u, 'profile'):
        Profile.objects.create(user=u, role='teacher') # Give admin a role just in case
        print("Profile created for admin.")
    else:
        print(f"Profile exists. Role: {u.profile.role}")

except Exception as e:
    print(f"ERROR: {e}")
