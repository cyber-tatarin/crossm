from django import forms
from .models import Countries
from django.db.models.fields import BLANK_CHOICE_DASH


def niche_choices():
    return [('Цветы', 'Цветы'),
            ('Стройка', 'Стройка')]


def country_choices():
    res = [(x.country, x.country) for x in Countries.objects.all().order_by('country')]
    return res


class CompanyCreateForm(forms.Form):
    title = forms.CharField(max_length=60, required=True)
    niche = forms.CharField(max_length=60, required=True, widget=forms.Select(choices=niche_choices()))

    country_of_res = forms.CharField(max_length=40, widget=forms.Select(choices=BLANK_CHOICE_DASH + country_choices()))
    link = forms.CharField(max_length=150)

    role = forms.CharField(max_length=60, required=True)
