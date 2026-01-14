import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import Subject

subjects = [
    "Математика",
    "Английский язык",
    "Информатика",
    "Физкультура",
    "География",
    "Геометрия",
    "Физика",
    "Химия",
    "Биология",
    "Русский язык",
    "Литература",
    "История",
    "Астрономия",
    "Зоология"
]

print("Starting to populate subjects...")

for name in subjects:
    subject, created = Subject.objects.get_or_create(name=name)
    if created:
        print(f"Created subject: {name}")
    else:
        print(f"Subject already exists: {name}")

print("Done.")
