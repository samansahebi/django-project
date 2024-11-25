from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order
from .serializers import ChargeUpOrderSerializer, ApproveChargeUpSerializer
import logging
from core.logging_formater import CustomFormatter


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

    def post(self):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'charge up request submitted by user: {self.request.user}')
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            logger.error(f'charge up request canceled: {serializer.errors}')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApproveChargeUp(APIView):
    serializer_class = ApproveChargeUpSerializer

    def post(self):
        user = self.request.user
        order = Order.objects.get(seller=user, id=self.request.data['id'])
        serializer = self.serializer_class(order, data=order, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(f'user {user.username} approved charge up: {serializer.data["amount"]}')
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            logger.error(serializer.errors)
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WaitingOrders(APIView):
    serializer_class = ChargeUpOrderSerializer

    def get(self):
        user = self.request.user
        order = Order.objects.filter(seller=user, is_approved=False)
        serializer = self.serializer_class(order, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
