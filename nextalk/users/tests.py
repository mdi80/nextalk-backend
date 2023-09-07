from django.test import TestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import User
from django.core.cache import cache

# Create your tests here.
# factory = APIRequestFactory()
# request = factory.post("/notes/", {"title": "new idea"})

# cache = {}


# class AuthTests(APITestCase):
#     def test_1_send_sms(self):
#         """
#         Ensure to get sms code for specified number.
#         """

#         url = reverse("sendsms")
#         data = {"phone": "+9893024"}
#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_2_check_sms(self):
#         """
#         Ensure to verify sms code.
#         """

#         url = reverse("checkcode")
#         data = {"phone": "+98912341234", "code": "123412"}
#         response = self.client.post(url, data, format="json")
#         cache["phone_key"] = response.data["key"]
#         self.assertEqual(response.data["new"], True)

#     def test_3_signup(self):

#         url = reverse("user-list")
#         data = {
#             "userid": "user",
#             "firstname": "test",
#             "lastname": "test",
#             "phone_key": cache["phone_key"],
#         }

#         response = self.client.post(url, data, format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
