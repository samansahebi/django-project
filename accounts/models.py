from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have an username')

        if not password:
            raise ValueError('Users must have an password')

        user = self.model(
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.active = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


class PhoneNumber(models.Model):
    user = models.ManyToManyField(User)
    phone_number = models.TextField(unique=True, name=False, blank=False)
    charge = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.phone_number


class Seller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=False, related_name='sellers')
    customers = models.ManyToManyField(User, blank=True)
    credit = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username


class Order(models.Model):
    amount = models.PositiveIntegerField(blank=False, null=False)
    is_approved = models.BooleanField(default=False)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.PROTECT, blank=False, null=False)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, blank=False, null=False)
    buyer = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, null=False)
    created_at = models.DateTimeField(auto_created=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'amount: {self.amount}, created at: {self.created_at}'
