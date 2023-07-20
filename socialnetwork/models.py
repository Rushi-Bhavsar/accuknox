from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone
Q = models.Q


class CustomerUserManager(BaseUserManager):

    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError('email field can not be empty.')
        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields, is_active=True)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)

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


class ConnectionRequest(models.Model):
    sender_user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='sender_user')
    receiver_user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='receiver_user')
    status = models.CharField(max_length=20, default='pending')
    request_time = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f'{self.pk}'

    @classmethod
    def create_connection_request(cls, from_user, to_user):
        """
        Create new connection request.
        :param from_user: MyUser Instance
        :param to_user: MyUser Instance
        :return: Newly created instance.
        """
        return cls.objects.create(sender_user=from_user, receiver_user=to_user, request_time=timezone.now())

    @classmethod
    def check_request_already_send(cls, from_user, to_user):
        first_condition = {'sender_user': from_user, 'receiver_user': to_user}
        second_condition = {'sender_user': to_user, 'receiver_user': from_user}
        return cls.objects.filter(Q(**first_condition) | Q(**second_condition)).exclude(status='reject')

    @classmethod
    def number_of_request(cls, from_user, time_range):
        return cls.objects.filter(sender_user=from_user, request_time__range=time_range, status='pending').count()


class Connection(models.Model):
    from_user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='from_user')
    to_user = models.ForeignKey(to=MyUser, on_delete=models.CASCADE, related_name='to_user')
    connection_date = models.DateField(auto_now=True)
    description = models.TextField()

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f'{self.pk}'

    @classmethod
    def check_connection_present(cls, from_user, to_user):
        first_condition = {'from_user': from_user, 'to_user': to_user}
        second_condition = {'from_user': to_user, 'to_user': from_user}
        return cls.objects.get(Q(**first_condition) | Q(**second_condition))
