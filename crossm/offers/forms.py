from django import forms
from .models import Offers


class CreateOfferForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Offers
        fields = ['coupon_price', 'currency', 'retail_price', 'title',
                  'amount', 'type']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите название услуги'
            }),
            'coupon_price': forms.DecimalField(decimal_places=2, attrs={
                'class': 'input input-300px',
                'placeholder': 'Введите цену купона'
            }),
            'currency': forms.Select(choices=[], attrs={
                'class': 'js-choice',
            }),
            'retail_price': forms.DecimalField(decimal_places=2, attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите розничную цену'
            }),
            'amount': forms.TextInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите название услуги'
            }),
            'type': forms.TextInput(attrs={
                'class': 'input input-620px',
                'placeholder': 'Введите название услуги'
            })
        }