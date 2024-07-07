import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager


class User(AbstractBaseUser):
    userId = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.EmailField(
        unique=True, error_messages={"unique": "User with email already exists"}
    )
    phone = models.CharField(max_length=15, null=True, blank=True)
    organisations = models.ManyToManyField("organisation.Organisation", blank=True)
    last_login = None

    REQUIRED_FIELDS = ["firstName", "lastName"]
    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email
