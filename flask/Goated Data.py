import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
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

# Load dataset

businessData = pd.read_csv('hacklyticsData.csv')
# Check dataset structure

#ESTIMATED FOOT TRAFFIC SCORE CREATION SECTION

def pointGeneratingFunction(E,P,N):
    # Select Features (X) and Target (y)
    X = businessData[[' Estimated Foot Traffic']]  # Replace with relevant feature names
    y = businessData['EFT Scores']  # Replace with the actual target column

    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Create Decision Tree Model
    model = RandomForestClassifier(n_estimators=100, max_depth=5,random_state = 42)  # I LOVE RANDOM FOREST
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)

    # Evaluate performance
    #print("Accuracy:", metrics.accuracy_score(y_test, y_pred))
    #print(metrics.classification_report(y_test, y_pred))

    # SCORE CREATION STUFF
    new_data = np.array([[E]])  # Use var to store generated Estimated Foot Traffic
    predicted_scoreEFT = model.predict(new_data)




    #POPULATION DENSITY SCORE CREATION SECTION

    # Select Features (X) and Target (y)
    X = businessData[['Population Density']]  # Replace with relevant feature names
    y = businessData['PD Scores']  # Replace with the actual target column

    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create Decision Tree Model
    model = RandomForestClassifier(n_estimators=100, max_depth=5,random_state = 42)  # I LOVE RANDOM FOREST
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)


    # SCORE CREATION STUFF
    new_data = np.array([[P]])  # Use var to store generated Estimated Foot Traffic
    predicted_scorePD = model.predict(new_data)

    #NEAREST COMPETITOR DISTANCE SCORE CREATION SECTION

    # Select Features (X) and Target (y)
    X = businessData[[' Nearest Competitor Distance']]  # Replace with relevant feature names
    y = businessData['NCD Scores']  # Replace with the actual target column

    # Split dataset into training (80%) and testing (20%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create Decision Tree Model
    model = RandomForestClassifier(n_estimators=100, max_depth=5,random_state = 42)  # I LOVE RANDOM FOREST
    model.fit(X_train, y_train)

    # Predict on test set
    y_pred = model.predict(X_test)


    # SCORE CREATION STUFF
    new_data = np.array([[N]])  # Use var to store generated Estimated Foot Traffic
    predicted_scoreNCD = model.predict(new_data)
    return([predicted_scoreEFT,predicted_scorePD,predicted_scoreNCD])

industry = "Restaurant"
preferences = [0.45,0.25,0.3]
address = " 26 5th St NW, Atlanta, GA 30332"


inputs = [address,industry,preferences]

def get_business_data(address, industry, GOOGLE_API_KEY, foursquare_api_key):
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
        type=industry
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
    

    genai.configure(api_key=gemini_api_key) #Added API Key
    model = genai.GenerativeModel('gemini-pro')

    prompt = f"What is the population density at the address: {address}. Return only the number, with no text. As in, do not write ANYTHING other than the number that is the population density."

    try:
        response = model.generate_content(prompt)
        # Correctly extract the text from the response
        try:
            population_density = response.candidates[0].content.parts[0].text.strip()
            # Remove commas before converting to float
            population_density = population_density.replace(",", "")
            population_density = float(population_density)
        except (AttributeError, IndexError): #Catch if the response is malformed.
            population_density = "Population Data Unavailable"

        try:
            population_density = float(population_density)
        except ValueError:
            population_density = "Population Data Unavailable"
        except Exception as e:
            print(f"Error converting to float: {e}")
            population_density = "Population Data Unavailable"

    except Exception as e:
        print(f"Error with Gemini API: {e}")
        population_density = "Population Data Unavailable"

    return {
        "Nearest Competitor Distance": float(distance[:-3]),
        "Estimated Foot Traffic": foot_traffic,
        "Population Density": population_density
    }

def mainFunction(address,industry):
    distance,foot_traffic,population_density = get_business_data(address, industry, os.getenv("GOOGLE_API_KEY"), os.getenv("FOURSQUARE_API_KEY")).values()  #You maybe need to add the API keys as real arguments
    Score1,Score2,Score3 = pointGeneratingFunction(foot_traffic,population_density,distance)
    indexScore = Score1*preferences[0] + Score2*preferences[1] + Score3*preferences[2]
    genai.configure(api_key=gemini_api_key) #Added API Key
    model = genai.GenerativeModel('gemini-pro') #the part starting here hopefully creates the description
    prompt = f"I need you to generate a description of the location at {address} as a potential location to start a business. Other than your own information on the business at that address, I have created a scoring system that I want you to use in your description. Never say the exact scores but use the data they provide to give insidght into the location. The scores are based on the following: Estimated Foot Traffic, Population Density, and Nearest Competitor Distance. A score closer to 100 is good and one farther away is bad. This location has a score of {Score1} for estmated foot traffic, {Score2} for population density, and {Score3} for the distance to its nearest competitor. Please use this information to create a description of the location."
    try:
        response = model.generate_content(prompt)
        # Correctly extract the text from the response
        try:
            description = response.candidates[0].content.parts[0].text.strip() #This part was from previous code and hopefully extracts the text. time will tell if it works.
        except (AttributeError, IndexError): #Catch if the response is malformed.
            description = "Description Unavailable"
    except Exception as e:
        print(f"Error with Gemini API: {e}")
        description = "Description Unavailable"
    return([{"description":description,"score":indexScore}])

 