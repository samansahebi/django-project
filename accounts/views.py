from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ChargeUpSerializer


class ChargeUp(APIView):
    serializer_class = ChargeUpSerializer

    def post(self):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            return Response(data="", status=status.HTTP_200_OK)
        else:
            return Response(data="", status=status.HTTP_400_BAD_REQUEST)
