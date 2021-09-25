from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)

from core.models import TimestampedModel


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, name, nickname, password=None, **extra_fields):
        if not email:
            raise ValueError("must have user email")
        if not phone_number:
            raise ValueError("must have user phone_number")
        if not name:
            raise ValueError("must have user name")
        if not nickname:
            raise ValueError("must have user nickname")
        
        user = self.model(
            email = self.normalize_email(email),
            phone_number = phone_number,
            name = name,
            nickname = nickname
        )
        return user
    
    def create_superuser(self, email, phone_number, name, nickname, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, phone_number, name, nickname, password, **extra_fields)


class User(AbstractBaseUser, TimestampedModel):
    email = models.EmailField(max_length=254, unique=True)
    phone_number = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    nickname = models.CharField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["nickname", "phone_number", "name"]

    def __str__(self):
        return self.nickname


class Follow(TimestampedModel):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")

    class Meta:
        db_table = "follow"