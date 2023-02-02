from django.db import models
from users.models import User
# Create your models here.


class Countries(models.Model):
    country = models.CharField(max_length=30)


class Companies(models.Model):
    title = models.CharField(max_length=60, null=False, blank=False)
    niche = models.CharField(max_length=60, null=False, blank=False)

    country_of_res = models.ForeignKey(Countries, on_delete=models.SET_NULL, null=True, blank=True)
    link = models.TextField(blank=True, null=True)

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=60, null=False, blank=False)

    unique_code = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length=20,  null=True, blank=True)

