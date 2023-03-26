from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from django_resized import ResizedImageField

from .managers import CustomUserManager


class Cities(models.Model):
    city = models.CharField(max_length=24)


class User(AbstractUser):
    NEWBIE = 1
    COMPLETE = 2
    MEMBER = 3
    
    ROLE_CHOICES = (
        (NEWBIE, 'Newbie'),
        (COMPLETE, 'Complete'),
        (MEMBER, 'Member'),
    )
    
    username = None
    email = models.EmailField(_('email address'), unique=True)

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=False, default=NEWBIE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def natural_key(self):
        return (self.first_name, self.last_name,)


class Profile(models.Model):
    phone_num = PhoneNumberField(null=False, blank=False, unique=True)
    phone_num_show = models.BooleanField(default=0)
    bio = models.CharField(max_length=200, blank=True, null=True)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = ResizedImageField(size=[500, 500], crop=['middle', 'center'], quality=99,
                              blank=True, null=True, upload_to='images')

    # Create your models here.
