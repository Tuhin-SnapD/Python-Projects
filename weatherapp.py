"""
Enhanced Weather App

A feature-rich weather application with multiple API support,
units selection, error handling, and improved user experience.
"""

import requests
import json
import sys
import time
from typing import Optional

# You can add more API keys and endpoints here
API_CONFIGS = [
    {
        'name': 'WeatherAPI',
        'url': 'https://api.weatherapi.com/v1/current.json',
        'key': '15e46681e2fb4ae089e202030232903',
        'city_param': 'q',
        'temp_path': ['current', 'temp_c'],
        'unit': 'C',
    },
    # Add more APIs if desired
]


def get_weather(city: str, api_config: dict, units: str = 'C') -> Optional[float]:
    params = {
        api_config['city_param']: city,
        'key': api_config['key']
    }
    try:
        response = requests.get(api_config['url'], params=params, timeout=10)
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
        data = response.json()
        temp = data
        for key in api_config['temp_path']:
            temp = temp[key]
        if units == 'F':
            return temp * 9/5 + 32
        return temp
    except Exception as e:
        print(f"❌ Failed to fetch weather: {e}")
        return None


def main():
    print("🌦️  ENHANCED WEATHER APP 🌦️")
    print("=" * 30)
    print("You can check the current temperature for any city.")
    print("=" * 30)
    
    while True:
        city = input("Enter the name of your city (or 'quit' to exit): ").strip()
        if city.lower() == 'quit':
            print("👋 Goodbye!")
            break
        
        print("Select units:")
        print("1. Celsius (°C)")
        print("2. Fahrenheit (°F)")
        unit_choice = input("Choose units (1 or 2, default 1): ").strip()
        units = 'F' if unit_choice == '2' else 'C'
        
        # Try all APIs in order
        temp = None
        for api_config in API_CONFIGS:
            temp = get_weather(city, api_config, units)
            if temp is not None:
                break
        
        if temp is not None:
            print(f"The temperature in {city.title()} is {temp:.1f}°{units}.")
        else:
            print(f"Could not retrieve weather for {city.title()}.")
        
        time.sleep(1)


if __name__ == "__main__":
    main()