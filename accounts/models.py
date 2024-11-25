from django.db import models
from django.contrib.auth.models import User


class Users(User):
    username = models.CharField(max_length=50)

    def __str__(self):
        return self.username

    def list(self):
        pass


class PhoneNumber(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=11, unique=True)
    charge = models.PositiveIntegerField()

    def __str__(self):
        return self.phone_number


class Seller(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False, null=False)
    customers = models.ManyToManyField(Users, blank=False, null=False)
    credit = models.PositiveIntegerField()

    def __str__(self):
        return self.user


class Order(models.Model):
    amount = models.PositiveIntegerField(blank=False, null=False)
    is_approved = models.BooleanField(default=False)
    phone_number = models.ForeignKey(PhoneNumber, on_delete=models.PROTECT, blank=False, null=False)
    seller = models.ForeignKey(Seller, on_delete=models.PROTECT, blank=False, null=False)
    buyer = models.ForeignKey(Users, on_delete=models.PROTECT, blank=False, null=False)
    created_at = models.DateTimeField(auto_created=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'amount: {self.amount}, created at: {self.created_at}'
