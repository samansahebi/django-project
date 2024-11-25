from django.urls import path
from .views import ChargeUpOrder, ApproveChargeUp, WaitingOrders


urlpatterns = [
    path('charge-up/', ChargeUpOrder.as_view(), name='charge_up'),
    path('approve-charge-up/', ApproveChargeUp.as_view(), name='approve_charge_up'),
    path('waiting-orders/', WaitingOrders.as_view(), name='waiting_orders'),
]
