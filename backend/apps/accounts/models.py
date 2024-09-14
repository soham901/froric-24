from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    coins = models.PositiveIntegerField(default=0)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.email
    
    # Method to add coins
    def add_coins(self, amount):
        self.coins += amount
        self.save()

    # Method to subtract coins
    def subtract_coins(self, amount):
        if self.coins >= amount:
            self.coins -= amount
            self.save()
        else:
            raise ValueError("Not enough coins")
    

class BasicRoleDemo(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='role')
    role_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.email} - {self.role_name}"
