from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import Users


class ChargeUpTests(APITestCase):
    def test_charge_up_order(self):
        self.client.force_login(Users.objects.get(id=1))
        url = reverse('charge-up')
        data = {'data': 'test'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_approve_charge_up_order(self):
        self.client.force_login(Users.objects.get(id=1))
        url = reverse('approve-charge-up')
        data = {'is_approved': True}
        headers = {'is_approved': True}
        response = self.client.post(url, data, headers=headers, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
