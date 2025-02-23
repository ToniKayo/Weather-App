import requests
from flask import Flask, render_template, request

app = Flask(__name__)

API_KEY = "Your_api_key"  # Your OpenWeatherMap API Key

def get_weather(city):
    if not city:
        return {"error": "Please enter a city name."}

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an error for bad responses (4xx, 5xx)
        data = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Network error: {e}"}
    
    # Check if API response contains expected data
    if data.get("cod") != 200:
        return {"error": f"City not found. Please try again."}

    return {
        "city": data.get("name", city),  # Fallback to input city name
        "country": data.get("sys", {}).get("country", "Unknown"),
        "temperature_c": data.get("main", {}).get("temp", "N/A"),
        "temperature_f": round((data.get("main", {}).get("temp", 0) * 9/5) + 32, 2),
        "description": data.get("weather", [{}])[0].get("description", "No description").capitalize(),
        "humidity": data.get("main", {}).get("humidity", "N/A"),
        "wind_speed": data.get("wind", {}).get("speed", "N/A"),
        "icon": data.get("weather", [{}])[0].get("icon", "")
    }

@app.route("/", methods=["GET", "POST"])
def home():
    weather = None
    if request.method == "POST":
        city = request.form.get("city", "").strip()  # Ensure input is trimmed and not empty
        if city:
            weather = get_weather(city)
    
    return render_template("index.html", weather=weather)

if __name__ == "__main__":
    app.run(debug=True)
