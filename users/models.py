from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    email = models.EmailField(unique=True)

    username = models.CharField(max_length=20, unique=True,
                                help_text="Required. 20 characters or fewer. Latin letters, digits and -/_ only.",
                                validators=[RegexValidator(
                                    r"^[a-zA-Z0-9_-]+\Z",
                                    "Enter a valid username. This value may contain only latin letters, numbers, and -/_ characters."
                                )],
                                error_messages={
                                    "unique": "A user with that username already exists.",
                                },
    )

    phone = models.CharField(max_length=20, null=True, blank=True, validators=[
            RegexValidator(
                r'^\+?1?\d{9,15}$',
                'Enter a valid phone number please.'
            )
        ])

    # image = models.ImageField(upload_to='profile_images',
    #                           null=True,
    #                           blank=True,
    #                           default='profile_images/default.png'
    #                           )

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'
        ordering = ['email']

    def __str__(self):
        return self.email
