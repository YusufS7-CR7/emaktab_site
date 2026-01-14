import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import Subject

# Names to target
targets = ['Math', 'Mathematics', 'Математика']

for name in targets:
    deleted_count, _ = Subject.objects.filter(name__iexact=name).delete()
    if deleted_count > 0:
        print(f"Deleted {deleted_count} subject(s) named '{name}'")
    else:
        print(f"No subject found named '{name}'")
