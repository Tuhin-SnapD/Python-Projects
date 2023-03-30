""" 
This code is a simple program that fetches the current weather data for a user-specified city using an API provided by WeatherAPI.

First, the user is prompted to enter the name of a city. The program then constructs a URL for the API request by inserting the city name into the 
URL string. The program then sends a GET request to the API using the constructed URL and stores the response in the response variable.

The program checks the status code of the response to ensure that the API request was successful. If it wasn't successful, an error message is 
printed. If the request was successful, the program parses the JSON response using the json.loads() method and extracts the temperature in Celsius 
from the response data.

Finally, the program prints the temperature in Celsius along with the name of the city entered by the user. 
"""

# Import necessary modules
import requests
import json

# Prompt user to enter city name
city = input("Enter the name of your city: ")

# Create API URL
url = f"https://api.weatherapi.com/v1/current.json?key=15e46681e2fb4ae089e202030232903&q={city}"

# Send API request
response = requests.get(url)

# Check if response was successful
if response.status_code != 200:
    print("Error occurred while fetching weather data.")
else:
    # Parse JSON response
    weather_data = json.loads(response.text)

    # Extract temperature in Celsius
    temperature_celsius = weather_data["current"]["temp_c"]

    # Print temperature in Celsius
    print(
        f"The temperature in {city} is {temperature_celsius} degrees Celsius.")