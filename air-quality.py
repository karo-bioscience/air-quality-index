import requests
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

API_KEY = 'bff9acaf8459b92ca4de4e419370cb40'
BASE_URL = 'http://api.openweathermap.org/data/2.5/air_pollution'

class AirQualityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Air Quality Monitor")
        
        self.label_lat = tk.Label(root, text="Latitude:")
        self.label_lat.pack()
        self.entry_lat = tk.Entry(root)
        self.entry_lat.pack()
        self.label_lon = tk.Label(root, text="Longitude:")
        self.label_lon.pack()
        self.entry_lon = tk.Entry(root)
        self.entry_lon.pack()
        
        self.button = tk.Button(root, text="Get Air Quality", command=self.get_air_quality)
        self.button.pack()
        self.result_label = tk.Label(root, text="")
        self.result_label.pack()
        self.plot_button = tk.Button(root, text="Plot Data", command=self.plot_data)
        self.plot_button.pack()

    def get_air_quality(self):
        lat = self.entry_lat.get()
        lon = self.entry_lon.get()
        try:
            lat = float(lat)
            lon = float(lon)
            data = self.fetch_air_quality(lat, lon)
            if data:
                processed_data = self.process_data(data)
                self.result_label.config(text=f"PM2.5: {processed_data['PM2.5']}, PM10: {processed_data['PM10']}, NO2: {processed_data['NO2']}, AQI: {processed_data['AQI']}")
                self.processed_data = processed_data  # Zapisz dane do późniejszego użycia
            else:
                messagebox.showerror("Error", "Failed to retrieve data")
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter valid latitude and longitude.")

    def fetch_air_quality(self, lat, lon):
        response = requests.get(BASE_URL, params={
            'lat': lat,
            'lon': lon,
            'appid': API_KEY
        })
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("Error: Unauthorized (check your API key)")
            return None
        else:
            print(f"Error: Unable to fetch data (status code: {response.status_code})")
            return None

    def process_data(self, data):
        if 'list' in data:
            components = data['list'][0]['components']
            aqi = data['list'][0]['main']['aqi']
            return {
                'PM2.5': components['pm2_5'],
                'PM10': components['pm10'],
                'NO2': components['no2'],
                'AQI': aqi
            }
        else:
            print("Error: No data available")
            return None

    def plot_data(self):
        if hasattr(self, 'processed_data'):
            processed_data = self.processed_data
            pollutants = ['PM2.5', 'PM10', 'NO2']
            concentrations = [processed_data[pollutant] for pollutant in pollutants]

            plt.bar(pollutants, concentrations)
            plt.xlabel('Pollutant')
            plt.ylabel('Concentration')
            plt.title('Air Quality')
            plt.show()
        else:
            messagebox.showerror("Error", "No data available to plot")

if __name__ == '__main__':
    root = tk.Tk()
    app = AirQualityApp(root)
    root.mainloop()
