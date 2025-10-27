import requests
import json
import time

# --- API Endpoints ---
# Open-Meteo Geocoding API: Used to convert city names to coordinates (Latitude/Longitude)
API_URL_GEO = 'https://geocoding-api.open-meteo.com/v1/search'
# Open-Meteo Weather API: Used to fetch weather data using coordinates
API_URL_WEATHER = 'https://api.open-meteo.com/v1/forecast'

def get_wind_direction(deg):
    """Converts wind degrees (0-360) to cardinal direction."""
    directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    # Round the degree to the nearest 45 degree interval and modulus by 8
    index = round(deg / 45) % 8
    return directions[index]

def fetch_with_retry(url, params=None, retries=3):
    """Utility to handle API requests with exponential backoff."""
    for i in range(retries):
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status() # Raise HTTPError for bad responses (4xx or 5xx)
            return response.json()
        except requests.exceptions.RequestException as e:
            if i < retries - 1:
                delay = 2 ** i
                print(f"⚠️ Request failed ({e}). Retrying in {delay} second(s)...")
                time.sleep(delay)
            else:
                raise

def fetch_weather(city_name):
    """Fetches and displays the current weather for the given city."""
    print(f"\nSearching for weather in '{city_name}'...")
    
    try:
        # --- Step 1: Geocoding (City Name to Coordinates) ---
        geo_params = {
            'name': city_name,
            'count': 1,
            'language': 'en',
            'format': 'json'
        }
        geo_data = fetch_with_retry(API_URL_GEO, params=geo_params)

        if not geo_data.get('results'):
            print(f"❌ City '{city_name}' not found. Please check the spelling.")
            return

        location = geo_data['results'][0]
        lat = location['latitude']
        lon = location['longitude']
        
        # Construct display name (City, State/Admin, Country)
        display_name = location['name']
        if location.get('admin1'):
            display_name += f", {location['admin1']}"
        if location.get('country'):
            display_name += f", {location['country']}"

        # --- Step 2: Fetch Current Weather ---
        weather_params = {
            'latitude': lat,
            'longitude': lon,
            'current_weather': 'true',
            'temperature_unit': 'celsius',
            'wind_speed_unit': 'kmh',
            'timezone': 'auto'
        }
        weather_data = fetch_with_retry(API_URL_WEATHER, params=weather_params)

        current_weather = weather_data.get('current_weather')

        if not current_weather:
            print("❌ Could not retrieve current weather data for this location.")
            return

        # Extract and format data
        temp = current_weather['temperature']
        wind_speed = current_weather['windspeed']
        wind_dir = current_weather['winddirection']
        time_updated = current_weather['time'].replace('T', ' ')
        
        wind_direction_str = get_wind_direction(wind_dir)

        # --- Display Results ---
        print("\n=============================================")
        print(f"  🌎 Weather in {display_name}")
        print("=============================================")
        print(f"  🌡️  Temperature: {temp}°C")
        print(f"  💨 Wind Speed: {wind_speed} km/h")
        print(f"  ➡️  Wind Direction: {wind_direction_str}")
        print(f"  ⏰ Last Updated: {time_updated}")
        print("=============================================")

    except requests.exceptions.HTTPError as err:
        print(f"❌ API Error: Failed to fetch data. Status code: {err.response.status_code}")
    except requests.exceptions.RequestException as err:
        print(f"❌ Network Error: Could not connect to the weather service. ({err})")
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")

def main():
    """Main application loop."""
    print("--- Python Weather CLI ---")
    print("Type 'exit' or 'quit' to close the application.")
    
    while True:
        city = input("\nEnter city name: ").strip()
        
        if city.lower() in ['exit', 'quit']:
            print("Goodbye! 👋")
            break
            
        if city:
            fetch_weather(city)
        else:
            print("Please enter a city name to search.")

if __name__ == "__main__":
    # Check for the required 'requests' library
    try:
        import requests
        main()
    except ImportError:
        print("\n========================================================")
        print("    ERROR: The 'requests' library is not installed.")
        print("    Please install it using: pip install requests")
        print("========================================================")
