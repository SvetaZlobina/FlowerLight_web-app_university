from django import forms
from django.core import exceptions
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from .models import Client, Product

FORM_ERROR_MESSAGES = {'required': 'Пожалуйста, заполните это поле'}


class LoginForm(forms.Form):
    login = forms.CharField(error_messages={'required': 'Пожалуйста, заполните это поле'},
                            widget=forms.TextInput(attrs={'placeholder': 'логин',
                                                          'class': 'form-control'}))
    password = forms.CharField(error_messages=FORM_ERROR_MESSAGES,
                               widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                 'placeholder': 'пароль'}))

    def user_login(self, request):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password']

        user = auth.authenticate(username=login, password=password)

        if user is not None and user.is_active:
            auth.login(request, user)
            return True

        else:
            self.add_error(None,
                           forms.ValidationError('Неверный логин или пароль'))
            return False


class RegisterForm(forms.Form):
    login = forms.CharField(label='Введите логин',
                            widget=forms.TextInput(attrs={'placeholder': 'логин',
                                                          'class': 'form-control'}),
                            min_length=5, max_length=20)
    password1 = forms.CharField(label='Введите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'пароль'}),
                                min_length=8, max_length=20)

    password2 = forms.CharField(label='Повторите пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'повтор пароля'}),
                                min_length=8, max_length=20)

    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control',
                                                         'placeholder': 'ФИО'}),
                           max_length=50)

    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control',
                                                            'placeholder': 'email'}),
                             max_length=50)

    phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'контактный телефон'}))

    address = forms.CharField(max_length=100, widget=forms.Textarea(attrs={'class': 'form-control',
                                                                           'placeholder': 'адрес',
                                                                           'rows': 2}))

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()

        if not valid:
            return valid

        login = self.cleaned_data['login']
        email = self.cleaned_data['email']
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            self.add_error(None,
                           forms.ValidationError('Пароли не совпадают'))
            return False

        elif User.objects.filter(username=login).exists():
            self.add_error(None,
                           forms.ValidationError('Пользователь с таким логином уже существует'))
            return False

        elif User.objects.filter(email=email).exists():
            self.add_error(None,
                           forms.ValidationError('Пользователь с таким email уже зарегистрирован'))
            return False

        else:
            return True

    def user_register(self):
        login = self.cleaned_data['login']
        password = self.cleaned_data['password1']
        email = self.cleaned_data['email']
        name = self.cleaned_data['name']
        phone = self.cleaned_data['phone']
        address = self.cleaned_data['address']

        try:
            User.objects.create_user(login, email, password)
            user = Client(name=name, login=login, email=email,
                          phone=phone, address=address)
            user.save()
        except BaseException:  # если вдруг что-то пошло не так
            return False

        return True


class ProductAddingForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'название',
                                                         'class': 'form-control'}),
                           max_length=50)
    type = forms.ChoiceField(choices=Product.PRODUCT_TYPE_CHOICES,
                             # default=Product.BOUQUET,
                             widget=forms.TextInput(attrs={'placeholder': 'тип',
                                                           'class': 'form-control'}), )
    price = forms.DecimalField(max_digits=8, decimal_places=2,
                               widget=forms.TextInput(attrs={'placeholder': 'цена за единицу',
                                                             'class': 'form-control'}), )
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control',
                                                               'placeholder': 'описание',
                                                               'rows': 2}))
    image = forms.ImageField()
