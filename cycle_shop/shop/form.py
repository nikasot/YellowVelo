from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm
from django.forms import EmailInput, CharField, PasswordInput, TextInput, ModelForm, Select, Textarea, FileInput, forms
from django import forms

from .models import Cycle


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].label = 'Наименование велосипеда'
        self.fields['category'].empty_label = 'Категория не выбрана'
        self.fields['description'].label = 'Описание'
        self.fields['price'].label = 'Цена велосипеда'
        self.fields['image'].label = 'Картинка'
        self.label_suffix = ''

    class Meta:
        model = Cycle
        fields = ['title', 'category', 'description', 'price', 'image']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Наименование велосипеда'
            }),
            'category': Select(attrs={
                'class': 'form-select',
                'placeholder': 'Категория'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Описание'
            }),
            'price': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Цена'
            }),
            'image': FileInput(attrs={
                'class': 'form-control',

            })
        }


class RegisterUserForm(UserCreationForm):
    email = CharField(
        label='Введите почту',
        widget=EmailInput(attrs={
            'class': 'form-control',
            'id': 'floatingInput'
        })
    )
    password1 = CharField(
        label='Введите пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'id': 'floatingPassword'
        })
    )
    password2 = CharField(
        label='Повторите пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'id': 'floatingPassword'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''

    class Meta:
        model = get_user_model()
        fields = ['email', 'password1', 'password2']


class LoginUserForm(AuthenticationForm):
    username = CharField(
        label='Почта',
        widget=EmailInput(attrs={
            'class': 'form-control',
            'id': 'floatingInput'
        })
    )
    password = CharField(
        label='Пароль',
        widget=PasswordInput(attrs={
            'class': 'form-control',
            'id': 'floatingPassword'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ''


class EmailChangeForm(forms.Form):
    """
    A form that lets a user change set their email while checking for a change in the
    e-mail.
    """
    error_messages = {
        'email_mismatch': ("The two email addresses fields didn't match."),
        'not_changed': ("The email address is the same as the one already defined."),
    }

    new_email1 = forms.EmailField(
        label=("Введите новый почтовый адрес"),
        widget=forms.EmailInput,
    )

    new_email2 = forms.EmailField(
        label=("Повторите новый почтовый адрес"),
        widget=forms.EmailInput,
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(EmailChangeForm, self).__init__(*args, **kwargs)

    def clean_new_email1(self):
        old_email = self.user.email
        new_email1 = self.cleaned_data.get('new_email1')
        if new_email1 and old_email:
            if new_email1 == old_email:
                raise forms.ValidationError(
                    self.error_messages['not_changed'],
                    code='not_changed',
                )
        return new_email1

    def clean_new_email2(self):
        new_email1 = self.cleaned_data.get('new_email1')
        new_email2 = self.cleaned_data.get('new_email2')
        if new_email1 and new_email2:
            if new_email1 != new_email2:
                raise forms.ValidationError(
                    self.error_messages['email_mismatch'],
                    code='email_mismatch',
                )
        return new_email2

    def save(self, commit=True):
        email = self.cleaned_data["new_email1"]
        self.user.email = email
        if commit:
            self.user.save()
        return self.user
