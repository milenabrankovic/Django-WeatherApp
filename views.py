from django.shortcuts import render
import requests
from .forms import CityForm

# Create your views here.

def index(request):
    city = 'Las Vegas'
    errors = []
    weather = {}

    if request.method == "POST":
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['name'].title()
    else:
        city = 'Las Vegas'

    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&units=imperial&appid=fcbd9f56b71fbb9def6cc909744d1d43'

    try:
        city_weather = requests.get(url.format(city)).json()
        weather = {
            'city': city,
            'country': city_weather['sys']['country'],
            'temperature_f': city_weather['main']['temp'],
            'temperature_c': fahrenheit_to_celsius(city_weather['main']['temp']),
            'feels_like': city_weather['main']['feels_like'],
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }
    except:
        errors.append(f'Sorry, the city "{city}" is not available in this weather map')

    form = CityForm()

    context = {
        'weather' : weather,
        'form': form,
        'errors': errors
    }

    return render(request, 'weatherApp/index.html', context)


def fahrenheit_to_celsius(temp):

    return int((temp  - 32) * 5/9)