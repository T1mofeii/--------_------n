from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Problem, Category

class RegistrationForm(UserCreationForm):
    phone = forms.CharField(required=False, label="Номер телефона")

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone', 'password1', 'password2']

class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput())
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput())

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {
            'name': 'Название категории'
        }

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'description', 'category', 'image_before']
        labels = {
            'title': 'Заголовок',
            'description': 'Описание проблемы',
            'category': 'Категория',
            'image_before': 'Фотография проблемы'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class ProblemUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        # Всегда показываем все статусы, включая "решена"
        self.fields['status'].choices = Problem.STATUS_CHOICES

    class Meta:
        model = Problem
        fields = ['status', 'rejection_reason', 'image_after']
        labels = {
            'status': 'Статус',
            'rejection_reason': 'Причина отклонения',
            'image_after': 'Фотография после решения'
        }
        widgets = {
            'rejection_reason': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'image_after': forms.FileInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        rejection_reason = cleaned_data.get('rejection_reason')
        image_after = cleaned_data.get('image_after')
        
        # Проверяем, что при отклонении указана причина
        if status == 'rejected' and not rejection_reason:
            raise forms.ValidationError('При отклонении заявки необходимо указать причину')
        
        # Проверяем, что при решении загружено фото "после"
        if status == 'solved':
            if not image_after and not self.instance.image_after:
                raise forms.ValidationError('Для решения заявки необходимо загрузить фото "после"')
        
        return cleaned_data
