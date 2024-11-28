from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import ChargeUpOrder, ApproveChargeUp, WaitingOrders


urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('charge-up', ChargeUpOrder.as_view(), name='charge-up'),
    path('approve-charge-up', ApproveChargeUp.as_view(), name='approve-charge-up'),
    path('waiting-orders', WaitingOrders.as_view(), name='waiting-orders'),
]
