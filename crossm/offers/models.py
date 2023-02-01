from django.db import models
from companies.models import Companies


class Offers(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)

    coupon_price = models.DecimalField(decimal_places=2, max_digits=6)
    currency = models.CharField(max_length=6)

    retail_price = models.DecimalField(decimal_places=2, max_digits=6)
    title = models.CharField(max_length=80)
    amount = models.IntegerField()


class OffersImages(models.Model):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/')
