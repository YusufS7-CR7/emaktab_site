from django import forms
from .models import Grade
from django.contrib.auth.models import User
from .models import Profile


class GradeForm(forms.ModelForm):
    student = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__role='student'),
        label="Ученик",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Grade
        fields = ['student', 'subject', 'value', 'comment']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'value': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
            'comment': forms.TextInput(attrs={'class': 'form-control'}),
        }

class RegisterForm(forms.ModelForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label="Пароль")
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES, label="Роль", widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя пользователя'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите ваше имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите вашу фамилию'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Придумайте пароль'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': 'Имя пользователя',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            # Signal creates profile, so we update it
            if hasattr(user, 'profile'):
                user.profile.role = self.cleaned_data['role']
                user.profile.save()
            else:
                Profile.objects.create(user=user, role=self.cleaned_data['role'])
        return user