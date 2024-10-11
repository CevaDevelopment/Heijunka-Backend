from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico debe ser proporcionado')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):

    ADMIN = 'admin'
    MANAGER = 'manager'
    EMPLOYEE = 'operator'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (EMPLOYEE, 'operator'),
    ]

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=50, default='null')
    last_name = models.CharField(max_length=50, default='null')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=EMPLOYEE)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Site(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class TypeClient(models.Model):
    MONOCLIENTE = 'mono'
    MULTICLIENTE = 'multi'

    TYPE_CHOICES = [
        (MONOCLIENTE, 'Monocliente'),
        (MULTICLIENTE, 'Multicliente'),
    ]

    name = models.CharField(max_length=10, choices=TYPE_CHOICES, unique=True)

    def __str__(self):
        return dict(self.TYPE_CHOICES).get(self.name, self.name)

class Client(models.Model):
    name = models.CharField(max_length=100)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True)
    type = models.ForeignKey(TypeClient, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

class Schedule(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    day_of_week = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.client.name} - {self.day_of_week} ({self.start_time} - {self.end_time})'


class TaskAssignment(models.Model):
    client = models.ForeignKey('Client', on_delete=models.CASCADE)
    task = models.TextField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()

    def __str__(self):
        return f"{self.client} - {self.task}"