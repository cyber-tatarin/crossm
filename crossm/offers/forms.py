from django import forms
from .models import Offers


class CreateOfferForm(forms.ModelForm):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

    class Meta:
        model = Offers
        fields = ['coupon_price', 'currency', 'retail_price', 'title',
                  'amount', 'type']
