import requests
import googlemaps
import os
from dotenv import load_dotenv
import google.generativeai as genai
import openai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
foursquare_api_key = os.getenv("FOURSQUARE_API_KEY")
gemini_api_key = os.getenv("GEMINI_API_KEY")
openai_api_key = os.getenv("OPENAI_API_KEY")

genai.configure(api_key=gemini_api_key)

atlanta_businesses = {
    "The Coca-Cola Company": ["1 Coca-Cola Plz NW, Atlanta, GA 30313", "Corporate Office"],
    "Delta Air Lines": ["1030 Delta Blvd, Atlanta, GA 30354", "Airline"],
    "UPS (United Parcel Service)": ["55 Glenlake Pkwy NE, Atlanta, GA 30328", "Logistics"],
    "The Home Depot": ["2455 Paces Ferry Rd NW, Atlanta, GA 30339", "Retail"],
    "Cox Enterprises": ["6205 Peachtree Dunwoody Rd, Atlanta, GA 30328", "Media/Communications"],
    "Georgia-Pacific": ["133 Peachtree St NE, Atlanta, GA 30303", "Manufacturing"],
    "Equifax": ["1550 Peachtree St NW, Atlanta, GA 30309", "Financial Services"],
    "NCR Corporation": ["864 Spring St NW, Atlanta, GA 30308", "Technology"],
    "Chick-fil-A": ["5200 Buffington Rd, Atlanta, GA 30349", "Restaurant"],
    "WestRock": ["1000 Abernathy Rd NE, Atlanta, GA 30328", "Packaging"],
    "Global Payments Inc.": ["3550 Lenox Rd NE, Atlanta, GA 30326", "Financial Services"],
    "PulteGroup": ["3350 Peachtree Rd NE, Atlanta, GA 30326", "Construction"],
    "Assurant": ["28 Liberty St, New York, NY 10005", "Insurance"], 
    "Veritiv": ["100 Mansell Ct E #300, Roswell, GA 30076", "Distribution"], 
    "Invesco": ["1555 Peachtree St NE, Atlanta, GA 30309", "Financial Services"],
    "Mary Mac's Tea Room": ["224 Ponce De Leon Ave NE, Atlanta, GA 30308", "Restaurant"],
    "The Varsity": ["61 North Ave NW, Atlanta, GA 30308", "Restaurant"],
    "Ponce City Market": ["675 Ponce De Leon Ave NE, Atlanta, GA 30308", "Market/Retail"],
    "Fox Bros. Bar-B-Q": ["1238 Dekalb Ave NE, Atlanta, GA 30307", "Restaurant"],
    "Staplehouse": ["745 Edgewood Ave SE, Atlanta, GA 30312", "Restaurant"],
    "Busy Bee Cafe": ["810 M.L.K. Jr Dr SW, Atlanta, GA 30314", "Restaurant"],
    "South City Kitchen": ["1144 Crescent Ave NE, Atlanta, GA 30309", "Restaurant"],
    "Miller Union": ["999 Brady Ave NW, Atlanta, GA 30318", "Restaurant"],
    "Antico Pizza Napoletana": ["1093 Hemphill Ave NW, Atlanta, GA 30318", "Restaurant"],
    "Waffle House": ["1767 Lakewood Ave SE, Atlanta, GA 30315", "Restaurant"], 
    "R Thomas Deluxe Grill": ["1818 Peachtree St NW, Atlanta, GA 30309", "Restaurant"],
    "Poor Calvin's": ["510 Piedmont Ave NE, Atlanta, GA 30308", "Restaurant"],
    "Gunshow": ["924 Garrett St SE, Atlanta, GA 30316", "Restaurant"],
    "Kimball House": ["303 E Howard Ave, Decatur, GA 30030", "Restaurant"],
    "The Optimist": ["914 Howell Mill Rd NW, Atlanta, GA 30318", "Restaurant"],
    "Lenox Square": ["3393 Peachtree Rd NE, Atlanta, GA 30326", "Shopping Mall"],
    "Phipps Plaza": ["3500 Peachtree Rd NE, Atlanta, GA 30326", "Shopping Mall"],
    "Atlantic Station": ["1380 Atlantic Dr NW, Atlanta, GA 30363", "Shopping/Entertainment"],
    "Little Five Points": ["1157 Euclid Ave NE, Atlanta, GA 30307", "Shopping District"],
    "Buckhead Village District": ["3035 Peachtree Rd NE, Atlanta, GA 30305", "Shopping/Entertainment"],
    "Trader Joe's": ["1845 Peachtree Rd NW, Atlanta, GA 30309", "Grocery Store"], 
    "Whole Foods Market": ["650 Ponce De Leon Ave NE, Atlanta, GA 30308", "Grocery Store"], 
    "Publix Super Markets": ["2139 Toco Hills Shopping Ctr, Atlanta, GA 30329", "Grocery Store"], 
    "Target": ["3535 Peachtree Rd NE, Atlanta, GA 30326", "Retail"], 
    "Walmart": ["835 M.L.K. Jr Dr NW, Atlanta, GA 30314", "Retail"], 
    "Georgia Aquarium": ["225 Baker St NW, Atlanta, GA 30313", "Attraction"],
    "World of Coca-Cola": ["121 Baker St NW, Atlanta, GA 30313", "Attraction"],
    "Atlanta Botanical Garden": ["1345 Piedmont Ave NE, Atlanta, GA 30309", "Attraction"],
    "Piedmont Park": ["400 Park Dr NE, Atlanta, GA 30306", "Park"],
    "Centennial Olympic Park": ["265 Park Ave W NW, Atlanta, GA 30313", "Park"],
    "The National Center for Civil and Human Rights": ["100 Ivan Allen Jr Blvd NW, Atlanta, GA 30313", "Museum"],
    "The Fox Theatre": ["660 Peachtree St NE, Atlanta, GA 30308", "Theater"],
    "The High Museum of Art": ["1280 Peachtree St NE, Atlanta, GA 30309", "Museum"],
    "Zoo Atlanta": ["800 Cherokee Ave SE, Atlanta, GA 30315", "Zoo"],
    "Martin Luther King Jr. National Historical Park": ["450 Auburn Ave NE, Atlanta, GA 30312", "Historical Site"],
    "Emory University": ["201 Dowman Dr, Atlanta, GA 30322", "University"],
    "Georgia Institute of Technology (Georgia Tech)": ["North Ave NW, Atlanta, GA 30332", "University"],
    "Piedmont Atlanta Hospital": ["1968 Peachtree Rd NW, Atlanta, GA 30309", "Hospital"],
    "Children's Healthcare of Atlanta": ["1405 Clifton Rd NE, Atlanta, GA 30322", "Hospital"], 
    "AT&T": ["303 Peachtree Center Ave NE, Atlanta, GA 30303", "Telecommunications"], 
    "Verizon": ["1163 Northside Dr NW, Atlanta, GA 30318", "Telecommunications"], 
    "Bank of America": ["600 Peachtree St NE, Atlanta, GA 30308", "Bank"], 
    "Wells Fargo": ["3535 Peachtree Rd NE, Atlanta, GA 30326", "Bank"], 
    "United States Postal Service": ["3900 Crown Rd SW, Atlanta, GA 30304", "Postal Service"], 
    "Atlanta City Hall": ["55 Trinity Ave SW, Atlanta, GA 30303", "Government"],
    "Hartsfield-Jackson Atlanta International Airport": ["6000 N Terminal Pkwy, Atlanta, GA 30320", "Airport"],
    "CNN Center": ["1 CNN Center NW, Atlanta, GA 30303", "Media"],
    "Mercedes-Benz Stadium": ["1 AMB Dr NW, Atlanta, GA 30313", "Stadium"],
    "Truist Park": ["755 Battery Ave SE, Atlanta, GA 30339", "Stadium"],
    "State Farm Arena": ["1 State Farm Dr, Atlanta, GA 30303", "Arena"]}

def get_business_data(address, business_type, GOOGLE_API_KEY, foursquare_api_key, openai_api_key):
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
    foot_traffic_response = requests.get(foursquare_url, headers=headers)
    
    if foot_traffic_response.status_code == 200:
        foot_traffic_data = foot_traffic_response.json()
        foot_traffic = len(foot_traffic_data.get("results", []))
    else:
        foot_traffic = "Unavailable"
    
    # Get population density using ChatGPT
    prompt = f"What is the population density at the address: {address}. Return only the number, with no text.As in, do not write ANYTHING other than the number that is the population density."
    try:
        response = openai.Completion.create(
            model="gpt-4",  # Or "gpt-4" if you have access to it
            messages=[{"role": "system", "content": "You are a helpful assistant."},
                      {"role": "user", "content": prompt}],
        )
        
        population_density = response['choices'][0]['message']['content'].strip()
        
        try:
            population_density = float(population_density)  # Attempt to convert to float
        except ValueError:
            population_density = "Population Data Unavailable"
    except Exception as e:
        print(f"Error with OpenAI API: {e}")
        population_density = "Population Data Unavailable"
    return {
        "Nearest Competitor Distance": distance,
        "Estimated Foot Traffic": foot_traffic,
        "Population Density": population_density
    }

# Example usage
business_address = "1600 Amphitheatre Parkway, Mountain View, CA"
business_category = "restaurant"  # Change based on business type

print(get_business_data(business_address, business_category, GOOGLE_API_KEY, foursquare_api_key, openai_api_key))

for business, data in atlanta_businesses.items():
    address, category = data
    dataset = {}
    dataset[business] = get_business_data(address, category, GOOGLE_API_KEY, foursquare_api_key, openai_api_key)

for business in dataset:
    ncd = dataset[business]['Nearest Competitor Distance']
    eft = dataset[business]['Estimated Foot Traffic']
    pd = dataset[business]['Population Density']
    fname = open("data.csv","a")
    fname.write(f"{business,ncd,eft,pd}")
    fname.readline()
    fname.close()
