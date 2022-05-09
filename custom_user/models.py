from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

# from app.api.security.custom_user_manager import CustomUserManager


class User(AbstractUser):
    STUDENT = 1
    CREATOR = 2
    STAFF = 3
    ADMIN = 4

    ROLE_CHOICES = (
        (STUDENT, "Student"),
        (CREATOR, "Creator"),
        (STAFF, "Staff"),
        (ADMIN, "Admin"),
    )

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    # username = None
    # email = models.EmailField("email address", unique=True)
    # USERNAME_FIELD = "email"
    # REQUIRED_FIELDS = []

    # objects = CustomUserManager()
