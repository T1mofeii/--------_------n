from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Problem

class RegistrationForm(UserCreationForm):
    phone = forms.CharField(required=False, label="Номер телефона")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'category', 'image_before']
        labels = {
            'title': 'Название проблемы',
            'description': 'Описание проблемы',
            'category': 'Категория',
            'image_before': 'Фотография проблемы'
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'image_before': forms.FileInput(attrs={'class': 'form-input'})
        }
