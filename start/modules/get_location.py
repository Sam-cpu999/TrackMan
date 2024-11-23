import requests

def get_location(ip):
    try:
        response = requests.get(f'https://ipinfo.io/{ip}/json')
        location_data = response.json()
        return f"{location_data.get('city', 'Unknown')}, {location_data.get('region', 'Unknown')}, {location_data.get('country', 'Unknown')}"
    except requests.RequestException:
        return 'Could not retrieve location'
