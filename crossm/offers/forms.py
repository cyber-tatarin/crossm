from django import forms
from .models import Offers
from django.db.models.fields import BLANK_CHOICE_DASH


def get_currency_choices():
    return [
        ('BYN', 'BYN'),
        ('RUB', 'RUB')
    ]


TYPE_CHOICES = [
    ('Товар', 'Товар'),
    ('Услуга', 'Услуга')
]


class CreateOfferForm(forms.ModelForm):
    image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={
        'multiple': True,
        'class': 'file-input',
        'id': 'choose-file-container',
        'accept': 'image/*'
    }))

    class Meta:
        model = Offers
        fields = ['coupon_price', 'currency', 'retail_price', 'title',
                  'amount', 'type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите название услуги'
            }),
            'coupon_price': forms.NumberInput(attrs={
                'class': 'input input-300px',
                'placeholder': 'Введите цену купона'
            }),
            'currency': forms.Select(choices=BLANK_CHOICE_DASH + get_currency_choices(), attrs={
                'class': 'js-choice',
            }),
            'retail_price': forms.NumberInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите розничную цену'
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите количество купонов'
            }),
            'type': forms.Select(choices=BLANK_CHOICE_DASH + TYPE_CHOICES, attrs={
                'class': 'js-choice',
            })
        }
