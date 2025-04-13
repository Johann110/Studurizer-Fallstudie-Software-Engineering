from django.contrib.auth import authenticate
from django.test import TestCase

from accounts.models import CustomUser


# Create your tests here.
class CustomUserTestcase(TestCase):
    def setUp(self):
        CustomUser.objects.create_user(username='test1', email='test@gmail.com', password='iamatest1234')
        CustomUser.objects.create_user(username='test2', email='test2@gmail.com', password='iamatest1234')
    def test_user_can_authenticate(self):
        user = CustomUser.objects.get(email='test@gmail.com')
        self.assertTrue(user.is_authenticated)
        user2 = CustomUser.objects.get(email='test2@gmail.com')
        self.assertTrue(user2.is_authenticated)
    def test_authenticating_works(self):
        user = authenticate(username='test@gmail.com', password='iamatest1234')
        self.assertTrue(user.is_authenticated)
