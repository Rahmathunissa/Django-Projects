import requests
from django.shortcuts import render
from .models import SearchHistory

API_KEY = "7389229b9e3a060912a1dd7406f27f60"

def index(request):
    weather = None
    error = None
    recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]  # last 5 searches

    if request.method == "POST":
        city = request.POST.get('city', '').strip()
        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            try:
                resp = requests.get(url, timeout=5)
                data = resp.json()

                if resp.status_code == 200:
                    weather = {
                        'city': f"{data['name']}, {data['sys']['country']}",
                        'temperature': data['main']['temp'],
                        'humidity': data['main']['humidity'],
                        'pressure': data['main']['pressure'],
                        'description': data['weather'][0]['description'].title(),
                        'icon': data['weather'][0]['icon'],
                    }
                    # Save search to DB
                    SearchHistory.objects.create(
                        city_name=data['name'],
                        temperature=data['main']['temp'],
                        humidity=data['main']['humidity'],
                        pressure=data['main']['pressure'],
                        description=data['weather'][0]['description'].title()
                    )
                    # Refresh recent searches
                    recent_searches = SearchHistory.objects.order_by('-searched_at')[:5]
                else:
                    error = data.get("message", "Could not fetch weather data.")
            except requests.RequestException:
                error = "Network error. Please try again."
        else:
            error = "Please enter a city name."

    return render(request, "main/index.html", {
        'weather': weather,
        'error': error,
        'recent_searches': recent_searches
    })