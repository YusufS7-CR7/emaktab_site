from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Subject, Profile, Grade
from .forms import GradeForm, RegisterForm


# =========================
# РЕГИСТРАЦИЯ
# =========================
from django.db.models import Q

# =========================
# РЕГИСТРАЦИЯ
# =========================
def register(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


# =========================
# ГЛАВНАЯ (РАСПРЕДЕЛЕНИЕ)
# =========================
@login_required(login_url='register')
def home_view(request):
    profile = getattr(request.user, 'profile', None)
    if not profile:
        messages.error(request, "Ошибка доступа: Профиль пользователя не найден.")
        return redirect('logout')
        
    if profile.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('subject_list')


# =========================
# ДЭШБОРД УЧЕНИКА
# =========================
@login_required(login_url='register')
def subject_list(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'student':
        return redirect('home')

    # Средний балл ТОЛЬКО для этого ученика
    subjects = Subject.objects.annotate(
        average=Avg('grades__value', filter=Q(grades__student=request.user))
    )

    # Вычисление цвета для каждого предмета
    for subject in subjects:
        if subject.average:
            # Нормализация: 2.0 -> 0 (красный), 5.0 -> 120 (зеленый)
            # Формула: (avg - 2) * (120 / (5 - 2)) = (avg - 2) * 40
            hue = (subject.average - 2) * 40
            # Ограничиваем от 0 до 120
            hue = max(0, min(120, hue))
            subject.color_hsl = f"hsl({hue}, 80%, 45%)"
        else:
            subject.color_hsl = "#6c757d" # серый

    return render(request, 'subjects_list.html', {
        'subjects': subjects,
        'student': request.user
    })


# =========================
# ДЕТАЛИ ПРЕДМЕТА (ОЦЕНКИ + КОММЕНТАРИИ)
# =========================
@login_required(login_url='register')
def subject_detail(request, subject_id):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'student':
        return redirect('home')

    subject = Subject.objects.get(id=subject_id)
    grades = subject.grades.filter(student=request.user).order_by('-date')

    return render(request, 'subject_detail.html', {
        'subject': subject,
        'grades': grades
    })


# =========================
# ДЭШБОРД УЧИТЕЛЯ
# =========================
@login_required(login_url='register')
def teacher_dashboard(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'teacher':
        return redirect('home')

    assigned_grades = Grade.objects.filter(teacher=request.user).order_by('-date')

    return render(request, 'teacher_dashboard.html', {
        'assigned_grades': assigned_grades
    })


# =========================
# ДОБАВЛЕНИЕ ОЦЕНКИ
# =========================
@login_required(login_url='register')
def add_grade(request):
    profile = getattr(request.user, 'profile', None)
    if not profile or profile.role != 'teacher':
        return HttpResponseForbidden('Только учитель может ставить оценки')

    if request.method == 'POST':
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.teacher = request.user
            grade.save()
            return redirect('teacher_dashboard')
    else:
        form = GradeForm()

    return render(request, 'add_grade.html', {'form': form})
