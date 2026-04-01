import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

# SAMPLE CLIMATE DATASET

data_dict = {
    "date": [
        "2024-01-01","2024-01-02","2024-01-03","2024-01-04",
        "2024-01-05","2024-01-06","2024-01-07","2024-01-08",
        "2024-01-09","2024-01-10"
    ],
    "temperature": [27,29,31,33,36,34,30,28,32,35],
    "humidity": [65,60,55,50,48,52,58,63,59,54],
    "wind_speed": [12,10,14,11,13,9,10,8,15,11],
    "rainfall": [0,2,0,0,1,0,3,4,0,2],
    "pressure": [1012,1010,1011,1009,1008,1013,1014,1012,1011,1010]
}

data = pd.DataFrame(data_dict)

# TEMPERATURE ANALYSIS

def average_temperature(data):
    temps = list(data["temperature"])
    avg = reduce(lambda a,b: a+b, temps) / len(temps)
    return avg

def max_temperature(data):
    return max(data["temperature"])

def min_temperature(data):
    return min(data["temperature"])

def detect_heatwaves(data):
    return list(filter(lambda x: x > 35, data["temperature"]))

# RAINFALL ANALYSIS

def total_rainfall(data):
    return sum(data["rainfall"])

def rainy_days(data):
    return list(filter(lambda x: x > 0, data["rainfall"]))

# HUMIDITY ANALYSIS

def average_humidity(data):
    return np.mean(data["humidity"])

# WIND ANALYSIS

def max_wind_speed(data):
    return max(data["wind_speed"])

def average_wind_speed(data):
    return np.mean(data["wind_speed"])

# PRESSURE ANALYSIS

def average_pressure(data):
    return np.mean(data["pressure"])

# CLIMATE INDEX (SIMPLE SCORE)

def climate_index(data):
    temp_score = np.mean(data["temperature"])
    humidity_score = np.mean(data["humidity"])
    wind_score = np.mean(data["wind_speed"])
    
    index = (temp_score + humidity_score + wind_score) / 3
    return index

# VISUALIZATION FUNCTIONS

def plot_temperature(data):
    plt.figure()
    plt.plot(data["date"], data["temperature"], marker="o")
    plt.title("Temperature Trend")
    plt.xlabel("Date")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_rainfall(data):
    plt.figure()
    plt.plot(data["date"], data["rainfall"], marker="o")
    plt.title("Rainfall Trend")
    plt.xlabel("Date")
    plt.ylabel("Rainfall (mm)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def plot_humidity(data):
    plt.figure()
    plt.plot(data["date"], data["humidity"], marker="o")
    plt.title("Humidity Trend")
    plt.xlabel("Date")
    plt.ylabel("Humidity (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# MAIN PROGRAM

def main():

    print("\nCLIMATE DATA ANALYSIS\n")

    print("Average Temperature:", round(average_temperature(data),2),"°C")
    print("Maximum Temperature:", max_temperature(data),"°C")
    print("Minimum Temperature:", min_temperature(data),"°C")
    print("Heatwave Days (>35°C):", detect_heatwaves(data))

    print("\nRainfall Statistics")
    print("Total Rainfall:", total_rainfall(data),"mm")
    print("Rainy Days:", rainy_days(data))

    print("\nHumidity Statistics")
    print("Average Humidity:", round(average_humidity(data),2),"%")

    print("\nWind Statistics")
    print("Max Wind Speed:", max_wind_speed(data),"km/h")
    print("Average Wind Speed:", round(average_wind_speed(data),2),"km/h")

    print("\nPressure Statistics")
    print("Average Pressure:", round(average_pressure(data),2),"hPa")

    print("\nClimate Index Score:", round(climate_index(data),2))

    print("\nGenerating Climate Graphs...")

    plot_temperature(data)
    plot_rainfall(data)
    plot_humidity(data)


if __name__ == "__main__":
    main()