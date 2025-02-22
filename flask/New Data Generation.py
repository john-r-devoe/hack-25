import requests
import googlemaps
import pandas as pd
import numpy as np


def get_business_data(address, business_type, GOOGLE_API_KEY, foursquare_api_key):
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    
    # Get coordinates of the address
    geocode_result = gmaps.geocode(address)
    if not geocode_result:
        return "Invalid address."
    
    location = geocode_result[0]['geometry']['location']
    lat, lng = location['lat'], location['lng']
    
    # Find nearest competitor using Google Places API
    places_result = gmaps.places_nearby(
        location=(lat, lng),
        radius=5000,  # Search within 5km
        type=business_type
    )
    
    if not places_result['results']:
        return "No competitors found nearby."
    
    nearest_competitor = places_result['results'][0]
    competitor_location = nearest_competitor['geometry']['location']
    
    # Calculate distance using Google Distance Matrix API
    distance_result = gmaps.distance_matrix(
        origins=f"{lat},{lng}",
        destinations=f"{competitor_location['lat']},{competitor_location['lng']}",
        mode="driving"
    )
    
    distance = distance_result['rows'][0]['elements'][0]['distance']['text']
    
    # Get foot traffic data from Foursquare API
    foursquare_url = f"https://api.foursquare.com/v3/places/search?ll={lat},{lng}&radius=500&categories=13000"
    headers = {"Authorization": foursquare_api_key, "Accept": "application/json"}
    foot_traffic_data = requests.get(foursquare_url, headers=headers).json()
    foot_traffic = len(foot_traffic_data.get("results", []))
    
    # Get population density (Example: US Census API - adjust as needed for other countries)
    census_url = f"https://api.census.gov/data/2020/pep/population?get=POP,NAME&for=tract:*&in=state:*&key=YOUR_CENSUS_API_KEY"
    population_data = requests.get(census_url).json()
    population_density = "Unknown"  # Processing logic needed based on geolocation
    
    return {
        "Nearest Competitor Distance": distance,
        "Estimated Foot Traffic": foot_traffic,
        "Population Density": population_density
    }

# Example usage
business_address = "1600 Amphitheatre Parkway, Mountain View, CA"
business_category = "restaurant"  # Change based on business type


print(get_business_data(business_address, business_category, GOOGLE_API_KEY, foursquare_api_key))
