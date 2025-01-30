from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import UserProfile, WeatherAlert
import requests

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            UserProfile.objects.create(user=user)
        return user

def get_weather_data(city):
    api_key = settings.OPENWEATHERMAP_API_KEY
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {
        'q': city,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    return response.json()

@login_required
def weather_view(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        weather_data = get_weather_data(city)
        
        if weather_data['cod'] == 200:
            context = {
                'city': city,
                'temperature': weather_data['main']['temp'],
                'humidity': weather_data['main']['humidity'],
                'wind_speed': weather_data['wind']['speed'],
                'description': weather_data['weather'][0]['description'],
                'weather_icon': get_weather_icon(weather_data['weather'][0]['main']),
            }
            return render(request, 'weather.html', context)
        else:
            messages.error(request, 'City not found. Please try again.')
    
    return render(request, 'weather.html')

@login_required
def add_favorite(request):
    if request.method == 'POST':
        city = request.POST.get('city')
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        if city not in profile.favorite_cities:
            profile.favorite_cities.append(city)
            profile.save()
            messages.success(request, f'{city} added to favorites.')
        else:
            messages.info(request, f'{city} is already in your favorites.')
    return redirect('weather')

@login_required
def favorites_view(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    favorite_cities = profile.favorite_cities
    weather_data = []
    
    for city in favorite_cities:
        data = get_weather_data(city)
        if data['cod'] == 200:
            weather_data.append({
                'city': city,
                'temperature': data['main']['temp'],
                'description': data['weather'][0]['description'],
                'weather_icon': get_weather_icon(data['weather'][0]['main']),
            })
    
    return render(request, 'favorites.html', {'weather_data': weather_data})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully. You can now log in.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def get_weather_icon(weather_condition):
    if weather_condition.lower() in ['clear', 'sunny']:
        return 'sun'
    elif weather_condition.lower() in ['rain', 'drizzle', 'thunderstorm']:
        return 'cloud-rain'
    elif weather_condition.lower() in ['clouds', 'mist', 'haze']:
        return 'cloud'
    elif weather_condition.lower() in ['snow']:
        return 'cloud-snow'
    else:
        return 'cloud-question'

