import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "Your_API_Key"  # Your OpenWeatherMap API Key

def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    print("API Response:", data)  # Debugging: Check API response in terminal

    if data["cod"] != 200:
        return {"error": "City not found. Please try again."}  # Fix: Return error properly

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temperature_c": data["main"]["temp"],
        "temperature_f": round((data["main"]["temp"] * 9/5) + 32, 2),
        "description": data["weather"][0]["description"].capitalize(),
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "icon": data["weather"][0]["icon"]
    }


@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        city = request.form["city"]
        weather = get_weather(city)
        print("Weather Data Sent to HTML:", weather)  # Debugging

    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
