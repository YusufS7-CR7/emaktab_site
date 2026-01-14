import os
import sys
import django
from django.conf import settings

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.core.management import call_command

with open('test_log.txt', 'w', encoding='utf-8') as f:
    try:
        call_command('test', 'app', stdout=f, stderr=f)
    except Exception as e:
        f.write(str(e))
