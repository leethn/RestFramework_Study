from django.db import models
from django.contrib.auth.models import BaseUserManager, \
    AbstractBaseUser, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(name, password, **extra_fields)

    def create_superuser(self, name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(name, password, **extra_fields)

    def _create_user(self, name, password, **extra_fields):
        if not name:
            raise ValueError('이름 넣어요')
        user = self.model(
            name=name,
            **extra_fields
        )
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=20, unique=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'name'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.name

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
