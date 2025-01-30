from django.test import TestCase
from django.contrib.auth.models import User
from .models import UserProfile, WeatherAlert

class WeatherAppTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.profile = UserProfile.objects.create(user=self.user)
        
    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.favorite_cities, [])

    def test_weather_alert_creation(self):
        alert = WeatherAlert.objects.create(
            user=self.user,
            city='Test City',
            alert_type='Test Type',
            message='Test Message'
        )
        self.assertEqual(alert.user, self.user)
        self.assertEqual(alert.city, 'Test City')
        self.assertEqual(alert.alert_type, 'Test Type')
        self.assertEqual(alert.message, 'Test Message')

