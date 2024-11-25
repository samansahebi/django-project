import logging
import rest_framework.exceptions
from rest_framework import serializers
from django.shortcuts import get_object_or_404
from .models import Order, Seller, Users, PhoneNumber
from core.logging_formater import CustomFormatter

# create logger with 'spam_application'
logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


class ChargeUpOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get('amount', None):

            logger.info("info message")
            return Order.objects.create(**validated_data)
        else:
            logger.error("error message")
            raise rest_framework.exceptions.ValidationError("")


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

    def update(self, instance, validated_data):
        seller = get_object_or_404(Seller, id=validated_data['seller'])
        buyer = get_object_or_404(Users, id=validated_data['buyer'])
        seller.credit -= validated_data['amount']
        if not seller.customers.filter(id=buyer.id).excists():
            seller.customers.add(buyer)
        seller.save()

        order = get_object_or_404(Order, id=validated_data['id'])
        order.is_approved = True
        order.save()

        phone_number = get_object_or_404(PhoneNumber, phone_number=validated_data['phone_number'])
        phone_number.charge += validated_data['amount']
        phone_number.save()

        logger.info("Order approved successfully")

        return {'', ''}
