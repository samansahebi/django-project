import logging
import rest_framework.exceptions
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Order, Seller, User, PhoneNumber
from core.logging_formater import CustomFormatter
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
            phone_number, _ = PhoneNumber.objects.get_or_create(phone_number=validated_data['phone_number'])
        except PhoneNumber.DoesNotExist:
            raise rest_framework.exceptions.ValidationError({"phone_number": "Phone Number does not exist"})
        validated_data['phone_number'] = phone_number
        return Order.objects.create(**validated_data)


class ApproveChargeUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def validate(self, data):
        seller = get_object_or_404(Seller, id=data['seller'])
        if data['amount'] > seller.credit:
            return data
        else:
            raise rest_framework.exceptions.ValidationError("seller credit is not enough")

    @transaction.atomic
    def update(self, instance, validated_data):
        seller = Seller.objects.select_for_update().get(id=validated_data['seller'])
        buyer = User.objects.select_for_update().get(id=validated_data['buyer'])
        seller.credit -= validated_data['amount']
        if not seller.customers.filter(id=buyer.id).excists():
            seller.customers.add(buyer)
        seller.save()

        order = Order.objects.select_for_update().get(id=validated_data['id'])
        order.is_approved = True
        order.save()

        phone_number = PhoneNumber.objects.select_for_update().get_or_create(phone_number=validated_data['phone_number'], user=buyer)
        phone_number.charge += validated_data['amount']
        phone_number.save()

        logger.info("Order approved successfully")

        return {'result', 'Order approved successfully'}
