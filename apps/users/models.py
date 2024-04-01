from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_regex = RegexValidator(
    regex=r'^998[0-9]{9}$',
    message="Phone number must be entered in the format: '998 [XX] [XXX XX XX]'. Up to 12 digits allowed."
)


class User(AbstractUser):
    LANGUAGES_CHOICES = (
        ('uz', 'Lotin'),
        ('oz', 'Uzbek'),
        ('ru', 'Russian'),
    )

    language = models.CharField(max_length=25, choices=LANGUAGES_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=13, validators=[phone_regex], blank=True, null=True, default=None)

    class Meta:
        ordering = ['-id']
