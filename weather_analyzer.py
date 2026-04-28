import os
from datetime import datetime, timedelta
from typing import Dict, List
import random

import matplotlib.pyplot as plt
import requests
import streamlit as st

# ---------------- CONFIG ----------------
API_KEY = os.getenv("OWM_API_KEY", "d74b3ba54bbfe029b565d455cafe0145")

CURRENT_WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "https://api.openweathermap.org/data/2.5/forecast"

WEATHER_ICONS = {
    "Clear": "☀️",
    "Clouds": "☁️",
    "Rain": "🌧️",
    "Drizzle": "🌦️",
    "Thunderstorm": "⛈️",
    "Snow": "❄️",
    "Mist": "🌫️",
}

# ---------------- API ----------------
def fetch_current_weather(city):
    try:
        res = requests.get(CURRENT_WEATHER_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })
        if res.status_code != 200:
            return None
        return res.json()
    except:
        return None

def fetch_forecast(city):
    try:
        res = requests.get(FORECAST_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })
        if res.status_code != 200:
            return None
        return res.json()
    except:
        return None

# ---------------- DATA ----------------
def parse_forecast(data):
    parsed = []
    for item in data["list"]:
        parsed.append({
            "time": datetime.fromtimestamp(item["dt"]),
            "temp": item["main"]["temp"],
            "humidity": item["main"]["humidity"],
            "rain": item.get("pop", 0) * 100
        })
    return parsed

def generate_week_data(current, forecast):
    today = datetime.now().date()
    week_data = []

    # ---------------- PAST 6 DAYS (SIMULATED) ----------------
    for i in range(6, 0, -1):
        date = today - timedelta(days=i)
        week_data.append({
            "date": date,
            "temp": current["main"]["temp"] + random.uniform(-3, 3),
            "humidity": current["main"]["humidity"] + random.uniform(-10, 10),
            "rain": random.uniform(0, 50)
        })

    # ---------------- TODAY ----------------
    week_data.append({
        "date": today,
        "temp": current["main"]["temp"],
        "humidity": current["main"]["humidity"],
        "rain": 0
    })

    # ---------------- FUTURE (PREDICTION) ----------------
    avg_temp = sum([i["temp"] for i in week_data]) / len(week_data)

    for i in range(1, 3):
        date = today + timedelta(days=i)
        week_data.append({
            "date": date,
            "temp": avg_temp + random.uniform(-2, 2),
            "humidity": current["main"]["humidity"],
            "rain": random.uniform(0, 60)
        })

    return week_data

# ---------------- GRAPHS ----------------
def plot_graph(x, y, title, ylabel):
    fig, ax = plt.subplots()  # Create a new figure properly
    ax.plot(x, y, marker='o')
    ax.set_title(title)
    ax.set_xlabel("Time")
    ax.set_ylabel(ylabel)
    plt.xticks(rotation=45)
    st.pyplot(fig)  # Pass the figure explicitly
    plt.close(fig)  # Close to free memory

# ---------------- INSIGHTS ----------------
def generate_insights(current, forecast):
    insights = []
    
    temp = current["main"]["temp"]
    humidity = current["main"]["humidity"]
    
    if temp > 35:
        insights.append("🔥 Very hot weather. Avoid afternoon travel.")
    elif temp < 10:
        insights.append("❄️ Very cold weather. Wear warm clothes.")
    else:
        insights.append("🌤 Pleasant weather for outdoor activities.")
    
    if humidity > 80:
        insights.append("💧 High humidity. It may feel uncomfortable.")
    
    # Best time
    best = min(forecast, key=lambda x: x["rain"])
    insights.append(f"📅 Best time to go out: {best['time'].strftime('%Y-%m-%d %H:%M')}")
    
    return insights

# ---------------- MAIN UI ----------------
def main():
    st.set_page_config(page_title="Weather Analyzer", page_icon="🌦️")
    st.title("🌦️ Weather Analyzer")
    
    city = st.text_input("Enter City Name")
    
    if st.button("Get Weather"):
        if not city:
            st.warning("Enter a city name")
            return
        
        with st.spinner("Fetching weather data..."):
            current = fetch_current_weather(city)
        
        if not current:
            st.error("City not found or API error")
            return
        
        condition = current["weather"][0]["main"]
        icon = WEATHER_ICONS.get(condition, "🌍")
        
        # Display current weather
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("🌡️ Temperature", f"{current['main']['temp']}°C")
        with col2:
            st.metric("💧 Humidity", f"{current['main']['humidity']}%")
        with col3:
            st.metric("☁️ Condition", f"{icon} {condition}")
        
        # Get forecast
        forecast_data = fetch_forecast(city)
        
        if not forecast_data:
            st.warning("No forecast available")
            return
        
        forecast = parse_forecast(forecast_data)
        times = [i["time"] for i in forecast[:10]]
        temps = [i["temp"] for i in forecast[:10]]
        humidity_data = [i["humidity"] for i in forecast[:10]]
        rain = [i["rain"] for i in forecast[:10]]
        
        # Display graphs
        st.subheader("📊 Temperature Forecast")
        plot_graph(times, temps, "Temperature Trend", "°C")
        
        st.subheader("📊 Humidity Forecast")
        plot_graph(times, humidity_data, "Humidity Trend", "%")
        
        st.subheader("📊 Rain Probability")
        plot_graph(times, rain, "Rain Probability", "%")
        
        # Display week data (optional)
        st.markdown("---")
        st.header("📅 Weekly Overview")
        week_data = generate_week_data(current, forecast)
        
        # Create a table for week data
        week_table = []
        for day in week_data:
            week_table.append({
                "Date": day["date"].strftime("%Y-%m-%d"),
                "Temperature": f"{day['temp']:.1f}°C",
                "Humidity": f"{day['humidity']:.0f}%",
                "Rain": f"{day['rain']:.1f}mm"
            })
        st.dataframe(week_table)
        
        # Insights
        st.markdown("---")
        st.header("🧠 Insights")
        
        insights = generate_insights(current, forecast)
        for tip in insights:
            st.info(tip)

if __name__ == "__main__":
    main()
