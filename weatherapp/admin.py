from django.contrib import admin
from .models import UserProfile, WeatherAlert

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_favorite_cities')
    
    def get_favorite_cities(self, obj):
        return ", ".join(obj.favorite_cities)
    get_favorite_cities.short_description = 'Favorite Cities'

@admin.register(WeatherAlert)
class WeatherAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'alert_type', 'created_at')
    list_filter = ('alert_type', 'created_at')
    search_fields = ('user__username', 'city', 'message')

