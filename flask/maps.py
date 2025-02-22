from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
import os, googlemaps, openai, random, math, json
from openai import OpenAI
import requests
from pathlib import Path
from datetime import datetime
import shutil
import time

load_dotenv()
app = Flask(__name__)
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
<title>Cool Maps Explorer</title>
<style>
body { margin: 0; padding: 0; height: 100vh; font-family: Arial, sans-serif; }
.container { height: 100vh; display: flex; flex-direction: column; }
.search-box { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 1000; display: flex; gap: 10px; background: white; padding: 15px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
#pac-input { width: 300px; padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
.view-toggle button { padding: 10px 15px; border: none; border-radius: 5px; cursor: pointer; background: #f0f2f5; transition: all 0.3s ease; }
.view-toggle button.active { background: #4285f4; color: white; }
#map { height: 100%; width: 100%; }
#result { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1); max-height: 400px; width: 80%; overflow-y: auto; font-size: 14px; line-height: 1.5; white-space: pre-wrap; }
</style>
</head>
<body>
<div class="container">
<div class="search-box">
<input id="pac-input" type="text" placeholder="Search for a place...">
<div class="view-toggle">
<button id="mapViewBtn" class="active">Map</button>
<button id="streetViewBtn">Street View</button>
<button id="analyzeBtn">Analyze</button>
</div>
</div>
<div id="map"></div>
<div id="result"></div>
</div>
<script>
let map, panorama, marker;
function initMap(){
const defaultLocation={lat:40.7128,lng:-74.0060};
map=new google.maps.Map(document.getElementById("map"),{zoom:12,center:defaultLocation,mapId:"8d193001f940fde3",streetViewControl:false});
panorama=new google.maps.StreetViewPanorama(document.getElementById("map"),{position:defaultLocation,pov:{heading:165,pitch:0},zoom:1});
panorama.setVisible(false);
const input=document.getElementById("pac-input");
const autocomplete=new google.maps.places.Autocomplete(input);
autocomplete.bindTo("bounds",map);
marker=new google.maps.Marker({map:map,animation:google.maps.Animation.DROP});
autocomplete.addListener("place_changed",()=>{
const place=autocomplete.getPlace();
if(!place.geometry||!place.geometry.location)return;
if(place.geometry.viewport){map.fitBounds(place.geometry.viewport);}else{map.setCenter(place.geometry.location);map.setZoom(17);}
marker.setPosition(place.geometry.location);
panorama.setPosition(place.geometry.location);
});
document.getElementById("mapViewBtn").addEventListener("click",()=>{
panorama.setVisible(false);
document.getElementById("mapViewBtn").classList.add("active");
document.getElementById("streetViewBtn").classList.remove("active");
});
document.getElementById("streetViewBtn").addEventListener("click",()=>{
panorama.setVisible(true);
document.getElementById("streetViewBtn").classList.add("active");
document.getElementById("mapViewBtn").classList.remove("active");
});
document.getElementById("analyzeBtn").addEventListener("click",()=>{
let center=map.getCenter();
fetch("/analyze",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({lat:center.lat(),lng:center.lng()})
}).then(response=>response.json()).then(data=>{
document.getElementById("result").innerText = data.analysis;
});
});
}
</script>
<script async defer src="https://maps.googleapis.com/maps/api/js?key={{ api_key }}&libraries=places&callback=initMap"></script>
</body>
</html>
'''
@app.route('/')
def index():
 return render_template_string(HTML_TEMPLATE, api_key=os.getenv("GOOGLE_API_KEY"))
def haversine(lat1, lon1, lat2, lon2):
 R=6371
 dLat=math.radians(lat2-lat1)
 dLon=math.radians(lon2-lon1)
 a=math.sin(dLat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dLon/2)**2
 c=2*math.atan2(math.sqrt(a), math.sqrt(1-a))
 return R*c

def get_top_businesses(businesses, limit=5):
    """Get top businesses based on rating and review count"""
    return sorted(
        [b for b in businesses if b.get('rating') and b.get('reviews')],
        key=lambda x: (x['rating'] * math.log(x['reviews'] + 1)),
        reverse=True
    )[:limit]

def generate_and_save_street_views(businesses, location_id):
    """Generate and save street view images for top businesses"""
    urls = []
    image_dir = Path("/Users/dhruvnarang/Desktop/hacklytics/pictures") / f"location_{location_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    image_dir.mkdir(parents=True, exist_ok=True)
    
    # Get top businesses and 2 images each
    top_businesses = get_top_businesses(businesses)
    images_per_business = 2
    total_images = 0
    
    for idx, business in enumerate(top_businesses):
        if total_images >= 10:  # Limit to 10 total images
            break
            
        lat = business.get("geometry", {}).get("location", {}).get("lat")
        lng = business.get("geometry", {}).get("location", {}).get("lng")
        name = business.get("name", "unknown")
        
        if not lat or not lng:
            continue
            
        # Get 2 angles for each business
        for angle in range(images_per_business):
            if total_images >= 10:
                break
                
            heading = angle * 180  # Get front and back views
            url = f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={lat},{lng}&heading={heading}&key={os.getenv('GOOGLE_API_KEY')}"
            urls.append({
                'url': url,
                'business_name': name,
                'rating': business.get('rating', 'N/A'),
                'reviews': business.get('reviews', 0)
            })
            
            # Download and save image
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                image_path = image_dir / f"{name.replace(' ', '_')}_{angle}.jpg"
                with open(image_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                total_images += 1
    
    return urls, str(image_dir)

def get_data_file_path():
    """Get absolute path for data.txt"""
    return os.path.join("/Users/dhruvnarang/Desktop/hacklytics", "data.txt")

def clean_business_for_storage(business):
    """Clean business data for storage by removing unnecessary fields"""
    return {
        "name": business.get("name"),
        "type": business.get("type"),
        "rating": business.get("rating"),
        "reviews": business.get("reviews"),
        "foot_traffic": business.get("foot_traffic"),
        "distance": business.get("distance"),
        "vicinity": business.get("vicinity"),
        "business_status": business.get("business_status")
    }

def store_analysis_data(lat, lng, data_payload, analysis):
    """Store both raw data and analysis, excluding unnecessary fields"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a clean copy of the data
    clean_data = {
        "location": data_payload["location"],
        "metrics": data_payload["metrics"],
        "businesses": [clean_business_for_storage(b) for b in data_payload["businesses"]],
        "image_directory": data_payload.get("image_directory")
    }
    
    data_file = get_data_file_path()
    if not os.path.exists(data_file):
        open(data_file, 'w').close()
        
    with open(data_file, "a", encoding='utf-8') as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"Location Analysis - {timestamp}\n")
        f.write(f"Coordinates: {lat}, {lng}\n")
        f.write(f"Images Directory: {clean_data.get('image_directory', 'N/A')}\n")
        f.write(f"\nRAW DATA:\n{json.dumps(clean_data, indent=2)}\n")
        f.write(f"\nANALYSIS:\n{analysis}\n")
        f.write(f"{'='*80}\n")

def get_last_analysis():
    """Get the most recent analysis and data from data.txt"""
    try:
        data_file = get_data_file_path()
        if not os.path.exists(data_file):
            return None
            
        with open(data_file, "r", encoding='utf-8') as f:
            content = f.read()
            sections = content.split("="*80)
            if not sections:
                return None
                
            # Get the last 3 analyses for context (or fewer if less available)
            recent_analyses = sections[-3:] if len(sections) >= 3 else sections
            formatted_analyses = []
            
            for section in recent_analyses:
                if not section.strip():
                    continue
                    
                # Extract coordinates, raw data, and analysis
                lines = section.strip().split('\n')
                timestamp = next((l for l in lines if "Location Analysis -" in l), "")
                coordinates = next((l for l in lines if "Coordinates:" in l), "")
                
                # Find the RAW DATA and ANALYSIS sections
                raw_data_start = section.find("RAW DATA:") + len("RAW DATA:")
                analysis_start = section.find("ANALYSIS:") + len("ANALYSIS:")
                
                raw_data = section[raw_data_start:section.find("ANALYSIS:")].strip()
                analysis = section[analysis_start:].strip()
                
                formatted_analyses.append({
                    "timestamp": timestamp,
                    "coordinates": coordinates,
                    "raw_data": raw_data,
                    "analysis": analysis
                })
                
            return formatted_analyses
            
    except Exception as e:
        print(f"Error reading data.txt: {e}")
        return None

def get_enhanced_location_data(lat, lng, location_id):
    """Get enhanced location data for exactly 75 closest businesses"""
    business_types = [
        "establishment", "store", "restaurant", "food", "doctor", "bank",
        "shopping_mall", "pharmacy", "health", "beauty_salon", "cafe", "gym"
    ]
    
    seen_places = set()
    combined_places = []
    
    # Get places for each business type
    for btype in business_types:
        try:
            places_result = gmaps.places_nearby(
                location=(lat, lng),
                rank_by="distance",
                type=btype
            )
            
            # Add unique places
            for place in places_result.get("results", []):
                if place['place_id'] not in seen_places and len(combined_places) < 75:
                    combined_places.append(place)
                    seen_places.add(place['place_id'])
            
            # If we have exactly 75 places, stop searching
            if len(combined_places) >= 75:
                break
                
        except Exception as e:
            print(f"Error fetching {btype} places: {str(e)}")
    
    # Process exactly 75 places (or fewer if not enough found)
    businesses = []
    total_foot_traffic = 0
    walking_volume = random.randint(5000, 15000)
    
    for place in combined_places[:75]:  # Limit to exactly 75
        try:
            place_details = gmaps.place(place['place_id'], fields=[
                'name', 'type', 'rating', 'user_ratings_total',
                'geometry/location', 'business_status',
                'formatted_address', 'vicinity', 'formatted_phone_number'
            ])['result']
            
            # Calculate distance
            plat = place_details["geometry"]["location"]["lat"]
            plng = place_details["geometry"]["location"]["lng"]
            distance = haversine(lat, lng, plat, plng)
            
            # Calculate foot traffic
            base_traffic = random.randint(100, 1000)
            rating_multiplier = float(place_details.get('rating', 3)) / 5
            distance_factor = 1 / (1 + distance)
            foot_traffic = int(base_traffic * rating_multiplier * distance_factor)
            
            total_foot_traffic += foot_traffic
            
            # Simplified business data structure
            businesses.append({
                "name": place_details.get("name"),
                "type": place_details.get("type", []),
                "rating": place_details.get("rating"),
                "reviews": place_details.get("user_ratings_total"),
                "foot_traffic": foot_traffic,
                "distance": round(distance, 2),
                "vicinity": place_details.get("vicinity"),
                "business_status": place_details.get("business_status"),
                "phone": place_details.get("formatted_phone_number") or ""
            })
            
        except Exception as e:
            print(f"Error processing place {place.get('name')}: {str(e)}")
            
    # Sort businesses by distance
    businesses.sort(key=lambda x: x.get('distance', float('inf')))
    
    # We still need geometry for street view generation, but only pass it to the function
    street_view_businesses = [{**b, "geometry": {"location": place_details["geometry"]["location"]}} 
                            for b in businesses[:50]]
    image_urls, image_dir = generate_and_save_street_views(street_view_businesses, location_id)
    
    return {
        "location": {"lat": lat, "lng": lng},
        "businesses": businesses,
        "street_view_images": image_urls,
        "image_directory": image_dir,
        "metrics": {
            "total_businesses": len(businesses),
            "average_rating": round(sum(b['rating'] for b in businesses if b.get('rating')) / len(businesses) if businesses else 0, 2),
            "average_distance": round(sum(b['distance'] for b in businesses) / len(businesses) if businesses else 0, 2),
            "total_foot_traffic": total_foot_traffic,
            "success_index": round(min(100, (
                (total_foot_traffic / (len(businesses) or 1)) / 100 * 0.4 +
                (5 - (sum(b['distance'] for b in businesses) / len(businesses) if businesses else 0)) * 10 * 0.3 +
                ((sum(b['rating'] for b in businesses if b.get('rating')) / len(businesses) if businesses else 0) * 10) * 0.3
            )), 2),
            "daily_walking_volume": walking_volume,
            "peak_hours_traffic": int(walking_volume * 0.2),
            "visual_coverage": "10 panoramic views of top-rated businesses",
            "total_searched_types": len(business_types),
            "total_unique_places_found": len(seen_places)
        }
    }

def get_last_analysis():
    """Get the most recent analysis and data from data.txt"""
    try:
        data_file = get_data_file_path()
        if not os.path.exists(data_file):
            return None
            
        with open(data_file, "r", encoding='utf-8') as f:
            content = f.read()
            sections = content.split("="*80)
            if not sections:
                return None
                
            # Get the last 3 analyses for context (or fewer if less available)
            recent_analyses = sections[-3:] if len(sections) >= 3 else sections
            formatted_analyses = []
            
            for section in recent_analyses:
                if not section.strip():
                    continue
                    
                # Extract coordinates, raw data, and analysis
                lines = section.strip().split('\n')
                timestamp = next((l for l in lines if "Location Analysis -" in l), "")
                coordinates = next((l for l in lines if "Coordinates:" in l), "")
                
                # Find the RAW DATA and ANALYSIS sections
                raw_data_start = section.find("RAW DATA:") + len("RAW DATA:")
                analysis_start = section.find("ANALYSIS:") + len("ANALYSIS:")
                
                raw_data = section[raw_data_start:section.find("ANALYSIS:")].strip()
                analysis = section[analysis_start:].strip()
                
                formatted_analyses.append({
                    "timestamp": timestamp,
                    "coordinates": coordinates,
                    "raw_data": raw_data,
                    "analysis": analysis
                })
                
            return formatted_analyses
            
    except Exception as e:
        print(f"Error reading data.txt: {e}")
        return None

def analyze_with_assistant(data_payload):
    """Analyze using fine-tuned assistant with memory"""
    try:
        print(f"Creating new thread...")
        thread = client.beta.threads.create()
        print(f"Thread created: {thread.id}")
        
        # Extract ALL text from data.txt
        data_file = get_data_file_path()
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                historical_data = f.read()
                if historical_data.strip():
                    print("Adding complete historical data...")
                    
                    # Send the historical data to the GPT model
                    context_msg = client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=f"Historical Analysis Data:\n\n{historical_data}"
                    )
                    print(f"Historical data message added: {context_msg.id}")
        
        # Add current location data
        print("Adding current location data...")
        current_analysis = f"""Analyze this new location with a focus on business potential:
1. Image Analysis: {len(data_payload.get('businesses', []))} nearby businesses have been photographed
2. Key Metrics: {json.dumps(data_payload['metrics'], indent=2)}
3. Top Businesses: {json.dumps(sorted(data_payload['businesses'], key=lambda x: x.get('rating', 0) or 0, reverse=True)[:5], indent=2)}

Based on the historical data and current analysis, please provide:
- Area characteristics and business environment
- Key success factors and opportunities
- Specific recommendations for business development
- Comparative analysis with previous locations
- Trends or patterns observed across different locations
"""
        
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=current_analysis
        )
        
        print("Starting assistant run...")
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=os.getenv("ASSISTANT_ID")
        )
        
        print(f"Waiting for completion. Run ID: {run.id}")
        while run.status not in ["completed", "failed"]:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            print(f"Run status: {run.status}")
            time.sleep(1)
            
        if run.status == "failed":
            error_msg = f"Analysis failed: {run.last_error}"
            print(error_msg)
            return error_msg
            
        print("Getting assistant response...")
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for msg in messages.data:
            if msg.role == "assistant":
                response = msg.content[0].text.value
                print(f"Got response of length: {len(response)}")
                return response
                
        return "No response from assistant"
        
    except Exception as e:
        error_msg = f"Analysis Error: {str(e)}"
        print(error_msg)
        return error_msg

def format_response(data_payload, analysis):
    """Format the response to only include the GPT analysis"""
    return {
        "analysis": analysis
    }

@app.route('/analyze', methods=["POST"])
def analyze():
    try:
        req = request.get_json()
        lat, lng = req["lat"], req["lng"]
        location_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"Starting analysis for location: {lat}, {lng}")
        
        # 1. First get the location data
        data_payload = get_enhanced_location_data(lat, lng, location_id)
        
        # 2. Store the data immediately, before analysis
        print("Storing data to data.txt...")
        store_analysis_data(lat, lng, data_payload, "Analysis pending...")
        
        # 3. Now analyze with the complete historical data
        print("Starting analysis with complete historical data...")
        analysis = analyze_with_assistant(data_payload)
        
        # 4. Update the analysis in data.txt
        print("Updating analysis in data.txt...")
        store_analysis_data(lat, lng, data_payload, analysis)
        
        return jsonify(format_response(data_payload, analysis))
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    required_vars = ["GOOGLE_API_KEY", "OPENAI_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        print(f"Missing environment variables: {', '.join(missing)}")
    else:
        app.run(debug=True)