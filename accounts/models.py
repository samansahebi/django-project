from django.db import models
from django.contrib.auth.models import User


class Users(User):
    username = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11)
    charge = models.ForeignKey("", on_delete=models.CASCADE, blank=False, null=False)
    is_seller = models.BooleanField()

    def __str__(self):
        return f'user name: {self.username}, phone number: {self.phone_number}, charge: {self.charge}'

    def list(self):
        pass


class Buyer(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.user


class Seller(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, blank=False, null=False)
    customers = models.ForeignKey(Buyer, on_delete=models.CASCADE, blank=False, null=False)

    def __str__(self):
        return self.user


class Order(models.Model):
    amount = models.IntegerField(blank=False, null=False)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, blank=False, null=False)
    buyer = models.ForeignKey(Buyer, on_delete=models.CASCADE, blank=False, null=False)
    created_at = models.DateTimeField(auto_created=True)

    def __str__(self):
        return f'amount: {self.amount}, created at: {self.created_at}'
