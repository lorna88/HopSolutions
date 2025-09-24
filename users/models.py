from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)

    phone = models.CharField(max_length=20, null=True, blank=True, validators=[
            RegexValidator(
                r'^\+?1?\d{9,15}$',
                'Введите корректный номер телефона.'
            )
        ])

    image = models.ImageField(upload_to='profile_images',
                              null=True,
                              blank=True,
                              default='profile_images/default.png'
                              )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
        ordering = ['email']

    def __str__(self):
        return self.email
