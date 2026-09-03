from flask import Flask
from flask import render_template
from flask import request
import requests

app = Flask(__name__)

API_KEY = 'fbf9bc3385fb77b7ce16b1bf1fdbe82e'

@app.route("/", methods=["GET", "POST"])

def index():
    weather_data = None
    error_message = None

    if request.method == "POST":
        city = request.form.get("city","").strip()

        if city:
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

            try:
                response = requests.get(url, timeout=5)

                if response.status_code == 200:
                                    data = response.json()
                                    weather_data = {
                                        "city": data["name"],
                                        "country": data["sys"]["country"],
                                        "temp": round(data["main"]["temp"]),
                                        "feels_like": round(data["main"]["feels_like"]),
                                        "description": data["weather"][0]["description"].title(),
                                        "icon": data["weather"][0]["icon"],
                                        "humidity": data["main"]["humidity"],
                                        "wind_speed": data["wind"]["speed"],
                                    }

                elif response.status_code == 404:
                        error_message = f"City '{city}' not found. Please check spelling."

                else:
                    error_message = "Unable to fetch data from weather service."
                    
            except requests.RequestException:
                error_message = "Connection error. Please try again later."
        else:
            error_message = "Please enter a city name."

    return render_template("index.html", weather=weather_data, error=error_message)

if __name__ == "__main__":
    app.run(debug=True)