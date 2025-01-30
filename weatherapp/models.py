from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_cities = models.JSONField(default=list)

class WeatherAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=100)
    alert_type = models.CharField(max_length=50)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

