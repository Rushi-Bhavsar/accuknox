from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager


class CustomerUserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('email field can not be empty.')
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff = True')

        if other_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser = True')

        return self.create_user(email, password, **other_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = CustomerUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class ConnectionRequest:
    request = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    sender = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='pending')
    request_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.pk}'


class Connection:
    customer_1 = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    customer_2 = models.ForeignKey(to=MyUser, on_delete=models.CASCADE)
    request_date = models.DateField(auto_now=True)
    description = models.TextField()

    def __str__(self):
        return f'{self.pk}'