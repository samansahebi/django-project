import logging
import random
import time

import rest_framework.exceptions
from rest_framework import serializers
from .models import Order, Seller, User, PhoneNumber
from core.logging_formater import CustomFormatter
from django.db import connection
from django.db import transaction


# create logger with 'spam_application'
logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


class PhoneNumberSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField("get_phone_number")

    class Meta:
        model = PhoneNumber
        fields = 'phone_number'


class ChargeUpOrderSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='phone_number.phone_number', max_length=11)

    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        try:
            phone_number, created = PhoneNumber.objects.select_for_update().get_or_create(phone_number=validated_data['phone_number'])
            if created:
                phone_number.user.add(self.context['user'])
        except PhoneNumber.DoesNotExist:
            raise rest_framework.exceptions.ValidationError({"phone_number": "Phone Number does not exist"})
        validated_data['phone_number'] = phone_number
        return Order.objects.select_for_update().create(**validated_data)


class ApproveChargeUpSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='phone_number.phone_number', max_length=11)

    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        try:
            if data.get('amount') < data.get('seller').credit:
                return data
            else:
                raise rest_framework.exceptions.ValidationError("seller credit is not enough")
        except serializers.ValidationError:
            raise rest_framework.exceptions.ValidationError({"amount": "Amount must be greater than seller credit"})

    def update(self, instance, validated_data):
        with transaction.atomic():
            order = Order.objects.select_related('seller', 'phone_number', 'buyer'
                                                 ).select_for_update().get(id=instance.id)

            if order:
                if not order.is_approved:
                    order.is_approved = True
                else:
                    raise rest_framework.exceptions.ValidationError("order is already approved")
                order.seller.credit -= instance.amount
                if not order.seller.customers.filter(id=instance.buyer.id):
                    order.seller.customers.add(order.buyer)
                if order.buyer != order.phone_number.user:
                    order.phone_number.user.add(order.buyer)
                order.phone_number.charge += instance.amount
                order.save()

                logger.info("Order approved successfully")

                return order

