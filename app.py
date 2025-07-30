# app.py
import os
import requests
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

API_KEY = os.getenv('OWM_API_KEY')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather = error = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
            r = requests.get(url)
            if r.status_code == 200:
                data = r.json()
                weather = {
                    'city': f"{data['name']}, {data['sys']['country']}",
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'humidity': data['main']['humidity'],
                    'wind': data['wind']['speed']
                }
            else:
                error = 'City not found. Please try again.'
        else:
            error = 'Please enter a city name.'
    return render_template('index.html', weather=weather, error=error)

if __name__ == '__main__':
    app.run(debug=True)

