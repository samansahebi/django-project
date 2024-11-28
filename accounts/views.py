import random
import time
from rest_framework import exceptions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, Seller, User
from .serializers import ChargeUpOrderSerializer, ApproveChargeUpSerializer
import logging
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


class ChargeUpOrder(APIView):
    serializer_class = ChargeUpOrderSerializer

    @transaction.atomic
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'user': request.user})
        if serializer.is_valid():
            serializer.save()
            logger.info(f'charge up order created by user: {request.user}')
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f'charge up request canceled: {serializer.errors}')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveChargeUp(APIView):
    serializer_class = ApproveChargeUpSerializer

    @transaction.atomic
    def post(self, request):
        for _ in range(5):
            order = Order.objects.select_for_update().filter(id=request.data['id'])
            if order.exists():
                serializer = self.serializer_class(order.first(), data=request.data, context={'user': request.user}, partial=True)

                if serializer.is_valid():
                    serializer.save()
                    logger.info(f'user approved charge up order: {serializer.data["amount"]}')
                    return Response(data=serializer.data, status=status.HTTP_200_OK)
                else:
                    logger.error(serializer.errors)
                    return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            else:
                time.sleep(random.uniform(1, 5))
                continue

        raise exceptions.NotFound()


class WaitingOrders(APIView):
    serializer_class = ChargeUpOrderSerializer

    def get(self, request):
        user = Seller.objects.get(user_id=request.user.id)
        order = Order.objects.filter(seller=user, is_approved=False)
        serializer = self.serializer_class(order, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
