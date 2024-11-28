from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from accounts.models import User, Order
import concurrent.futures


class ChargeUpTests(APITestCase):
    fixtures = ['./accounts/fixtures.json', ]

    def setUp(self):
        self.user = User.objects.get(username='saman')
        self.client.force_authenticate(self.user)

    def test_fixtures(self):
        print('test_fixtures')
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(Order.objects.count(), 2)

    def test_charge_up_order(self):

        def make_request():
            url = reverse('charge-up')
            data = {
                        "seller": 1,
                        "buyer": 2,
                        "phone_number": "09308848565",
                        "amount": "5000"
                    }
            response = self.client.post(url, data, format='json')
            return response.status_code
        res = make_request()
        self.assertEqual(res, status.HTTP_201_CREATED)
        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #     futures = [executor.submit(make_request) for _ in range(10)]
        #     for future in concurrent.futures.as_completed(futures):
        #         self.assertIn(future.result(), [status.HTTP_200_OK, status.HTTP_201_CREATED])

    def test_approve_charge_up_order(self):
        def make_request():
            url = reverse('approve-charge-up')
            data = {
                        "id": 3,
                        "seller": 1,
                        "amount": "5000"
                    }
            response = self.client.post(url, data=data, format='json')
            return response.status_code
        res = make_request()
        self.assertEqual(res, status.HTTP_200_OK)
        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #     futures = [executor.submit(make_request) for _ in range(10)]
        #     for future in concurrent.futures.as_completed(futures, timeout=5):
        #         self.assertIn(future.result(), [status.HTTP_200_OK, status.HTTP_201_CREATED])

