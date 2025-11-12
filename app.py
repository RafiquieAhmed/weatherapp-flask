from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "b4dec044e537e90207eebfc06ed4abdd" #enter your api key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            error = "Please enter a city name."
        else:
            # Build API request
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'  # or 'imperial' for Fahrenheit
            }
            response = requests.get(BASE_URL, params=params)

            if response.status_code == 200:
                data = response.json()
                weather = {
                    'city': data['name'],
                    'country': data['sys']['country'],
                    'temperature': round(data['main']['temp']),
                    'unit': 'C',
                    'description': data['weather'][0]['description'],
                    'icon_url': f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png",
                    'humidity': data['main']['humidity'],
                    'wind_speed': data['wind']['speed'],
                    'wind_unit': 'm/s',
                    'pressure': data['main']['pressure'],
                }
            else:
                error = "City not found or invalid API request."

    return render_template('weather.html', weather=weather, error=error)
    

if __name__ == '__main__':
    app.run(debug=True)
