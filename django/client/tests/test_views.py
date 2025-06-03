from django.contrib.auth.models import User

from client.models import Client, Historical

from decimal import Decimal

from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient, APITestCase


class ClientViewSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.client_test = Client.objects.create(
            name='client_test',
            debt='250.00'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        self.url_client = '/client/'
        self.url_put_delete = f"/client/{self.client_test.id}/"

    def test_get_all_clients_in_the_sistem(self):
        all_clients = self.client.get(self.url_client)
        self.assertEqual(all_clients.status_code, status.HTTP_200_OK)

    def test_create_new_client(self):
        new_client = {
            "name": "NewClient",
            "debt": "200.00"
        }
        post_client = self.client.post(self.url_client, new_client, format="json")
        self.assertEqual(post_client.status_code, status.HTTP_201_CREATED)

    def test_update_client(self):
        client = {
            "name": "UpdatedClient",
            "debt": "200.00"
        }
        put_client = self.client.put(self.url_put_delete, client, format="json")
        self.assertEqual(put_client.status_code, status.HTTP_200_OK)

        self.client_test.refresh_from_db()
        self.assertEqual(self.client_test.name, client["name"])
        self.assertEqual(self.client_test.debt, Decimal(client["debt"]))

    def test_delete_client(self):
        response = self.client.delete(self.url_put_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class HistoricalVieSetTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='123456')
        self.client_test = Client.objects.create(
            name='client_test',
            debt='250.00'
        )
        self.historical = Historical.objects.create(
            client=self.client_test,
            value="10.00",
            observation="Test Observation"
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        self.url_historical = '/historical/'
        self.url_put_delete_historical = f"/historical/{self.historical.id}/"

    def test_get_all_historical_in_the_sistem(self):
        all_historical = self.client.get(self.url_historical)
        self.assertEqual(all_historical.status_code, status.HTTP_200_OK)

    def test_create_historical_for_client_test(self):
        historical_test = {
            "client": self.client_test.id,
            "value": "10.00",
            "observation": "Unit Test"
        }
        response = self.client.post(self.url_historical, historical_test, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_historical(self):
        new_historical = {
            "client": self.client_test.id,
            "value": "250.00",
            "observation": "Update Historical"
        }
        response = self.client.put(self.url_put_delete_historical, new_historical, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_historical(self):
        response = self.client.delete(self.url_put_delete_historical)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
