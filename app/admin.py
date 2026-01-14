from django.contrib import admin
from .models import Subject, Grade


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('id', 'subject', 'value', 'date')
    list_filter = ('subject',)
