from django.urls import reverse
from django.test import TestCase
from django.utils import timezone

from .models import User

# Create your tests here.

class TestBlockedUser(TestCase):
    def test_user_blocking(self):
        url = reverse("users:index")
        
        for _ in range(10):
            response = self.client.get(url)
            if _ in range(6):
                self.assertEqual(response.status_code, 200)
            
        self.assertEqual(response.status_code, 403)
        
        
