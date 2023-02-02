from django import forms
from django.contrib.auth import password_validation
from django.db.models import BLANK_CHOICE_DASH
from django.utils.translation import gettext_lazy as _
from .models import User, Cities, Profile
from phonenumber_field.formfields import PhoneNumberField, RegionalPhoneNumberWidget
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from phonenumber_field.widgets import RegionalPhoneNumberWidget

choices = [(x.city, x.city) for x in Cities.objects.all().order_by('city')]


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'class': 'input input-340px',
            'placeholder': 'Введите пароль',
        }),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            'class': 'input input-400px',
            'placeholder': 'Повторите пароль',
        }),
        strip=False,
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите имя',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите фамилию',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input input-460px',
                'placeholder': 'Введите Email',
            }),
        }
        error_messages = {
            'email': {
                'unique': "Пользователь с таким адресом электронной почты уже существует"
            }
        }


class ProfileInfoForm(forms.Form):
    phone_num = PhoneNumberField(required=True, widget=RegionalPhoneNumberWidget(attrs={
        'class': 'input input-367px',
        'placeholder': 'Введите телефон',
    }))
    phone_num_show = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={
        'class': 'check-box',
    }))

    bio = forms.CharField(max_length=500, required=False, widget=forms.Textarea(attrs={
        'class': 'input-textarea',
        'wrap': 'soft',
        'placeholder': 'Введите описание'
    }))
    city = forms.CharField(initial="Не указывать", widget=forms.Select(choices=BLANK_CHOICE_DASH + choices,
                                                                       attrs={
                                                                           'class': "js-choice"
                                                                       }), required=True)

    def clean_phone_num(self):
        cleaned_phone_num = self.cleaned_data['phone_num']
        if Profile.objects.filter(phone_num=cleaned_phone_num).first():
            raise forms.ValidationError(
                "Этот номер телефона уже зарегистрирован")
        return cleaned_phone_num


class ProfileUpdateForm(ProfileInfoForm):

    def __init__(self, user_id_check, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_id_check = user_id_check

    first_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={
        'class': 'input input-620px',
        'placeholder': 'Введите имя'
    }))
    last_name = forms.CharField(max_length=60, required=True, widget=forms.TextInput(attrs={
        'class': 'input input-620px',
        'placeholder': 'Введите фамилию'
    }))

    def clean_phone_num(self):
        cleaned_phone_num = self.cleaned_data['phone_num']
        obj = Profile.objects.filter(phone_num=cleaned_phone_num).first()
        if obj:
            if obj.user.id != self.user_id_check:
                raise forms.ValidationError(
                    "Этот номер телефона уже зарегистрирован на другого пользователя")
        return self.cleaned_data['phone_num']


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(required=True,
                                widget=forms.EmailInput(attrs={'class': 'input input-620px',
                                                               'placeholder': 'Введите Email'}))

    password = forms.CharField(max_length=100, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'input input-620px',
                                                                 'placeholder': 'Введите пароль'}))
