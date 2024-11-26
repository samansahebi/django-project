from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User
import concurrent.futures


class ChargeUpTests(APITestCase):
    def test_charge_up_order(self):
        def make_request():
            self.client.force_login(User.objects.get(id=1))
            url = reverse('charge-up')
            data = {
                        "seller": 4,
                        "buyer": 2,
                        "phone_number": "09308848565",
                        "amount": "5000"
                    }
            response = self.client.post(url, data, format='json')
            return response.status_code

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            for future in concurrent.futures.as_completed(futures):
                self.assertIn(future.result(), [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_approve_charge_up_order(self):
        def make_request():
            self.client.force_login(User.objects.get(id=1))
            url = reverse('approve-charge-up')
            data = {'is_approved': True}
            headers = {'is_approved': True}
            response = self.client.post(url, data, headers=headers, format='json')
            return response.status_code

        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            for future in concurrent.futures.as_completed(futures):
                self.assertIn(future.result(), [status.HTTP_200_OK, status.HTTP_201_CREATED])
