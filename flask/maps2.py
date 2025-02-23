from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv
import os, googlemaps, openai, math, json, requests, shutil, time, random
from pathlib import Path
from datetime import datetime
from rich.console import Console

# Load environment variables
load_dotenv()
app = Flask(__name__)
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
console = Console()

# HTML template remains unchanged
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
    map=new google.maps.Map(document.getElementById("map"),{
        zoom:12,
        center:defaultLocation,
        mapId:"8d193001f940fde3",
        streetViewControl:false
    });
    panorama=new google.maps.StreetViewPanorama(document.getElementById("map"),{
        position:defaultLocation,
        pov:{heading:165,pitch:0},
        zoom:1
    });
    panorama.setVisible(false);
    const input=document.getElementById("pac-input");
    const autocomplete=new google.maps.places.Autocomplete(input);
    autocomplete.bindTo("bounds",map);
    marker=new google.maps.Marker({map:map,animation:google.maps.Animation.DROP});
    autocomplete.addListener("place_changed",()=>{
        const place=autocomplete.getPlace();
        if(!place.geometry||!place.geometry.location)return;
        if(place.geometry.viewport){
            map.fitBounds(place.geometry.viewport);
        }else{
            map.setCenter(place.geometry.location);
            map.setZoom(17);
        }
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

# Haversine distance function remains unchanged
def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

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
    # Create images directory relative to this file's folder
    base_dir = Path(__file__).parent
    image_dir = base_dir / "pictures" / f"location_{location_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    image_dir.mkdir(parents=True, exist_ok=True)

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

        for angle in range(images_per_business):
            if total_images >= 10:
                break

            heading = angle * 180  # front and back views
            url = f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={lat},{lng}&heading={heading}&key={os.getenv('GOOGLE_API_KEY')}"
            urls.append({
                'url': url,
                'business_name': name,
                'rating': business.get('rating', 'N/A'),
                'reviews': business.get('reviews', 0)
            })

            response = requests.get(url, stream=True)
            if response.status_code == 200:
                image_path = image_dir / f"{name.replace(' ', '_')}_{angle}.jpg"
                with open(image_path, 'wb') as f:
                    shutil.copyfileobj(response.raw, f)
                total_images += 1

    return urls, str(image_dir)

# Use relative path for data.txt in the same folder as this file
def get_data_file_path():
    return os.path.join(os.path.dirname(__file__), "data.txt")

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

            recent_analyses = sections[-3:] if len(sections) >= 3 else sections
            formatted_analyses = []

            for section in recent_analyses:
                if not section.strip():
                    continue
                lines = section.strip().split('\n')
                timestamp = next((l for l in lines if "Location Analysis -" in l), "")
                coordinates = next((l for l in lines if "Coordinates:" in l), "")
                raw_data_start = section.find("RAW DATA:") + len("RAW DATA:")
                analysis_start = section.find("ANALYSIS:") + len("ANALYSIS:")
                raw_data = section[raw_data_start:section.find("ANALYSIS:")].strip()
                analysis_text = section[analysis_start:].strip()

                formatted_analyses.append({
                    "timestamp": timestamp,
                    "coordinates": coordinates,
                    "raw_data": raw_data,
                    "analysis": analysis_text
                })

            return formatted_analyses

    except Exception as e:
        console.log(f"[red]Error reading data.txt:[/red] {e}")
        return None

def get_real_time_foot_data(lat, lng):
    """
    Retrieve real-time foot traffic data using the Foursquare API.
    (Note: This uses a fictional endpoint for illustration. Adjust according to actual API docs.)
    """
    try:
        headers = {
            "Accept": "application/json",
            "Authorization": os.getenv("FOOT_SQUARE_API_KEY")
        }
        params = {
            "ll": f"{lat},{lng}",
            "radius": 1000  # e.g., 1 km radius
        }
        # Fictional endpoint; replace with the real one if available
        response = requests.get("https://api.foursquare.com/v3/places/trending", headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            # For demonstration, sum up a hypothetical "totalCheckins" for trending places
            daily_walking_volume = sum(place.get("stats", {}).get("totalCheckins", 0) for place in data.get("results", []))
            if daily_walking_volume == 0:
                daily_walking_volume = 10000
            peak_hours_traffic = int(daily_walking_volume * 0.2)
            return {"daily_walking_volume": daily_walking_volume, "peak_hours_traffic": peak_hours_traffic}
        else:
            console.log(f"[red]Foursquare API error:[/red] {response.status_code}")
            return {"daily_walking_volume": 10000, "peak_hours_traffic": 2000}
    except Exception as e:
        console.log(f"[red]Foursquare API exception:[/red] {e}")
        return {"daily_walking_volume": 10000, "peak_hours_traffic": 2000}

def get_enhanced_location_data(lat, lng, location_id):
    """Get enhanced location data for exactly 75 closest businesses"""
    business_types = [
        "establishment", "store", "restaurant", "food", "doctor", "bank",
        "shopping_mall", "pharmacy", "health", "beauty_salon", "cafe", "gym"
    ]
    seen_places = set()
    combined_places = []

    for btype in business_types:
        try:
            places_result = gmaps.places_nearby(
                location=(lat, lng),
                rank_by="distance",
                type=btype
            )
            for place in places_result.get("results", []):
                if place['place_id'] not in seen_places and len(combined_places) < 75:
                    combined_places.append(place)
                    seen_places.add(place['place_id'])
            if len(combined_places) >= 75:
                break
        except Exception as e:
            console.log(f"[red]Error fetching {btype} places:[/red] {str(e)}")

    businesses = []
    total_foot_traffic = 0

    # Retrieve real-time foot data for the overall location
    foot_data = get_real_time_foot_data(lat, lng)
    walking_volume = foot_data["daily_walking_volume"]

    # Determine a base traffic value per business using real-time data
    num_businesses = len(combined_places[:75]) if combined_places[:75] else 1
    base_traffic_overall = walking_volume / num_businesses

    for place in combined_places[:75]:
        try:
            place_details = gmaps.place(place['place_id'], fields=[
                'name', 'type', 'rating', 'user_ratings_total',
                'geometry/location', 'business_status',
                'formatted_address', 'vicinity', 'formatted_phone_number'
            ])['result']

            plat = place_details["geometry"]["location"]["lat"]
            plng = place_details["geometry"]["location"]["lng"]
            distance = haversine(lat, lng, plat, plng)

            rating_multiplier = float(place_details.get('rating', 3)) / 5
            distance_factor = 1 / (1 + distance)
            # Use the overall base traffic to derive each business's foot traffic
            foot_traffic = int(base_traffic_overall * rating_multiplier * distance_factor)
            total_foot_traffic += foot_traffic

            businesses.append({
                "name": place_details.get("name"),
                "type": place_details.get("type", []),
                "rating": place_details.get("rating"),
                "reviews": place_details.get("user_ratings_total"),
                "foot_traffic": foot_traffic,
                "distance": round(distance, 2),
                "vicinity": place_details.get("vicinity"),
                "business_status": place_details.get("business_status"),
                "phone": place_details.get("formatted_phone_number") or "",
                "geometry": {"location": place_details["geometry"]["location"]}
            })

        except Exception as e:
            console.log(f"[red]Error processing place {place.get('name')}:[/red] {str(e)}")

    businesses.sort(key=lambda x: x.get('distance', float('inf')))
    street_view_businesses = businesses[:50]
    image_urls, image_dir = generate_and_save_street_views(street_view_businesses, location_id)

    metrics = {
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
        "peak_hours_traffic": foot_data["peak_hours_traffic"],
        "visual_coverage": "10 panoramic views of top-rated businesses",
        "total_searched_types": len(business_types),
        "total_unique_places_found": len(seen_places)
    }

    return {
        "location": {"lat": lat, "lng": lng},
        "businesses": businesses,
        "street_view_images": image_urls,
        "image_directory": image_dir,
        "metrics": metrics
    }

def analyze_with_assistant(data_payload):
    """Analyze using fine-tuned assistant with memory"""
    try:
        console.log("Creating new thread...")
        thread = client.beta.threads.create()
        console.log(f"Thread created: {thread.id}")

        data_file = get_data_file_path()
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                historical_data = f.read()
                if historical_data.strip():
                    console.log("Adding complete historical data...")
                    context_msg = client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=f"Historical Analysis Data:\n\n{historical_data}"
                    )
                    console.log(f"Historical data message added: {context_msg.id}")

        console.log("Adding current location data...")
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
        console.log("Starting assistant run...")
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=os.getenv("ASSISTANT_ID")
        )
        console.log(f"Waiting for completion. Run ID: {run.id}")
        while run.status not in ["completed", "failed"]:
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            console.log(f"Run status: {run.status}")
            time.sleep(1)

        if run.status == "failed":
            error_msg = f"Analysis failed: {run.last_error}"
            console.log(f"[red]{error_msg}[/red]")
            return error_msg

        console.log("Getting assistant response...")
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for msg in messages.data:
            if msg.role == "assistant":
                response = msg.content[0].text.value
                console.log(f"Got response of length: {len(response)}")
                return response

        return "No response from assistant"

    except Exception as e:
        error_msg = f"Analysis Error: {str(e)}"
        console.log(f"[red]{error_msg}[/red]")
        return error_msg

def format_response(data_payload, analysis):
    """Format the response to only include the GPT analysis"""
    return {"analysis": analysis}

@app.route('/analyze', methods=["POST"])
def analyze():
    try:
        req = request.get_json()
        lat, lng = req["lat"], req["lng"]
        location_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        console.log(f"Starting analysis for location: {lat}, {lng}")

        data_payload = get_enhanced_location_data(lat, lng, location_id)
        console.log("Storing data to data.txt...")
        store_analysis_data(lat, lng, data_payload, "Analysis pending...")
        console.log("Starting analysis with complete historical data...")
        analysis_text = analyze_with_assistant(data_payload)
        console.log("Updating analysis in data.txt...")
        store_analysis_data(lat, lng, data_payload, analysis_text)
        return jsonify(format_response(data_payload, analysis_text))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/data', methods=["GET"])
def send_data_file():
    """Send the entire contents of data.txt to the user."""
    data_file = get_data_file_path()
    if os.path.exists(data_file):
        with open(data_file, "r", encoding='utf-8') as f:
            content = f.read()
        return jsonify({"data": content})
    else:
        return jsonify({"error": "Data file not found."}), 404

if __name__ == "__main__":
    required_vars = ["GOOGLE_API_KEY", "OPENAI_API_KEY", "FOOT_SQUARE_API_KEY"]
    missing = [var for var in required_vars if not os.getenv(var)]
    if missing:
        console.log(f"[red]Missing environment variables:[/red] {', '.join(missing)}")
    else:
        app.run(debug=True)