from django.shortcuts import redirect
from django.urls import path
from .views import (
    register, 
    subject_list, 
    teacher_dashboard, 
    add_grade, 
    home_view,
    subject_detail
)
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    
    path('student/dashboard/', subject_list, name='subject_list'),
    path('student/subject/<int:subject_id>/', subject_detail, name='subject_detail'),
    path('teacher/dashboard/', teacher_dashboard, name='teacher_dashboard'),
    path('grade/add/', add_grade, name='add_grade'),
]
