from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date
from .models import UserProfile

class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        help_text="Введите уникальное имя пользователя. Максимальная длина 150 символов."
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Введите пароль. Длина пароля должна быть не менее 6 символов."
    )
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text="Введите вашу дату рождения в формате ГГГГ-ММ-ДД."
    )
    email = forms.EmailField(
        help_text="Введите ваш email. Допустимы только адреса с доменом @example.com."
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Пользователь с таким именем уже существует.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 6:
            raise ValidationError("Пароль должен быть не менее 6 символов.")
        return password

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        today = date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise ValidationError("Регистрация доступна только для пользователей старше 18 лет.")
        return birth_date

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise ValidationError("Регистрация доступна только для email-адресов с доменом @example.com.")
        if UserProfile.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email
