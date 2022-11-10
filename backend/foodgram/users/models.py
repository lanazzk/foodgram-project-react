from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomUser(AbstractUser):
    email = models.EmailField(
        max_length=254,
        unique=True)
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]',
            message='Invalid character in username.')
        ])
    first_name = models.CharField(
        max_length=150,)
    last_name = models.CharField(
        max_length=150,)
    password = models.CharField(
        max_length=150,)

    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'User'
        ordering = ['id']

    def __str__(self):
        return self.username
