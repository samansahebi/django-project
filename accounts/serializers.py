import logging
import rest_framework.exceptions
from rest_framework import serializers
from .models import Order
from core.logging_formater import CustomFormatter

# create logger with 'spam_application'
logger = logging.getLogger("My_app")
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

ch.setFormatter(CustomFormatter())

logger.addHandler(ch)


class ChargeUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get('', None):

            logger.info("info message")
            return Order.objects.create(**validated_data)
        else:
            logger.error("error message")
            raise rest_framework.exceptions.ValidationError("")
