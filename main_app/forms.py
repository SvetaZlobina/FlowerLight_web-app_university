from django import forms
from django.core import exceptions

from .models import Client


class LoginForm(forms.Form):
    error_css_class = 'error'
    login = forms.CharField(label='Введите логин',
                            widget=forms.TextInput(attrs={'placeholder': 'Логин',
                                                          'class': 'form-control'}))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'Пароль'}))

    def is_valid(self):
        valid = super(LoginForm, self).is_valid()

        if not valid:
            return valid

        login = self.cleaned_data['login']
        password = self.cleaned_data['password']

        try:
            client = Client.objects.get(login=login)
            if client.password == password:
                return True
            else:
                self.add_error(None,
                               forms.ValidationError('Неправильный пароль!'))
                return False
        except exceptions.ObjectDoesNotExist:
            self.add_error(None,
                           forms.ValidationError('Пользователя с таким логином не существует!'))
            return False
