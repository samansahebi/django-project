from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework.exceptions import ValidationError
from .models import Order


@receiver(pre_save, sender=Order)
def order_pre_save(sender, instance, **kwargs):
    order = Order.objects.filter(id=instance.id)
    if order.exists() and order.first().is_approved:
        raise ValidationError("this charge request is approved before")
