from django.db import models
from companies.models import Companies
from PIL import Image


class Offers(models.Model):
    company = models.ForeignKey(Companies, on_delete=models.CASCADE)
    type = models.CharField(max_length=30)
    
    coupon_price = models.DecimalField(decimal_places=2, max_digits=9)
    currency = models.CharField(max_length=6)
    
    retail_price = models.DecimalField(decimal_places=2, max_digits=10)
    title = models.CharField(max_length=80)
    amount_min = models.IntegerField(blank=False, null=True)
    amount_max = models.IntegerField(blank=False, null=True)
    
    has_photo = models.BooleanField(null=True)
    
    def natural_key(self):
        return (self.title,) + self.company.natural_key() + self.company.owner.natural_key()
    
    natural_key.dependencies = ['companies.companies', 'users.user']


class OffersImages(models.Model):
    offer = models.ForeignKey(Offers, on_delete=models.CASCADE)
    image = models.FileField(upload_to='images/')
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        instance = self
        image = Image.open(instance.image.path)
        image.save(instance.image.path, quality=60, optimize=True)
        return instance
