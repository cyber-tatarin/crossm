from django import forms
from .models import Offers


class CreateOfferForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={
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
            'currency': forms.Select(choices=[], attrs={
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
            'type': forms.TextInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите название услуги'
            })
        }
