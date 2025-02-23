from flask import Flask, render_template_string, request, jsonify, redirect, url_for, make_response
from dotenv import load_dotenv
import os, googlemaps, openai, random, math, json, requests, shutil, time
from pathlib import Path
from datetime import datetime
from fpdf import FPDF

import errno
from rich.console import Console
from rich.panel import Panel

console = Console()

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent
app = Flask(__name__)
gmaps = googlemaps.Client(key=os.getenv("GOOGLE_API_KEY"))
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SURVEY_HTML = '''
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Business Location Survey</title>
<style>
body { 
    font-family: 'Segoe UI', Arial, sans-serif;
    margin: 0;
    padding: 40px;
    background: #f5f7fa;
    color: #2c3e50;
}
.survey-container {
    max-width: 800px;
    margin: 0 auto;
    background: white;
    padding: 30px 40px;
    border-radius: 12px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
h1 {
    color: #2c3e50;
    margin-bottom: 30px;
    text-align: center;
    font-size: 2em;
}
.question-group {
    margin-bottom: 25px;
    padding: 15px;
    border-radius: 8px;
    background: #f8f9fa;
}
label {
    display: block;
    margin-bottom: 10px;
    font-weight: 600;
    color: #34495e;
}
select {
    width: 100%;
    padding: 12px;
    border: 2px solid #dde1e7;
    border-radius: 6px;
    font-size: 16px;
    color: #2c3e50;
    background: white;
    margin-bottom: 5px;
}
textarea {
    width: 100%;
    padding: 12px;
    border: 2px solid #dde1e7;
    border-radius: 6px;
    font-size: 16px;
    min-height: 120px;
    resize: vertical;
}
.hint {
    font-size: 14px;
    color: #7f8c8d;
    margin-top: 5px;
}
button {
    display: block;
    width: 100%;
    padding: 15px;
    background: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    font-size: 18px;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s ease;
}
button:hover {
    background: #2980b9;
}
</style>
</head>
<body>
<div class="survey-container">
    <h1>Business Location Analysis Survey</h1>
    <form method="POST" action="/submit_survey">
        <div class="question-group">
            <label>How important is foot traffic to your business? (1-5)</label>
            <select name="q1" required>
                <option value="">Select importance...</option>
                <option value="1">1 - Not important</option>
                <option value="2">2 - Slightly important</option>
                <option value="3">3 - Moderately important</option>
                <option value="4">4 - Very important</option>
                <option value="5">5 - Extremely important</option>
            </select>
            <div class="hint">Consider how much your business relies on walk-in customers</div>
        </div>

        <div class="question-group">
            <label>What's your priority level for being near complementary businesses? (1-5)</label>
            <select name="q2" required>
                <option value="">Select priority...</option>
                <option value="1">1 - Not a priority</option>
                <option value="2">2 - Low priority</option>
                <option value="3">3 - Medium priority</option>
                <option value="4">4 - High priority</option>
                <option value="5">5 - Essential priority</option>
            </select>
            <div class="hint">Example: A café might benefit from being near offices or retail shops</div>
        </div>

        <div class="question-group">
            <label>How important is parking availability? (1-5)</label>
            <select name="q3" required>
                <option value="">Select importance...</option>
                <option value="1">1 - Not important</option>
                <option value="2">2 - Slightly important</option>
                <option value="3">3 - Moderately important</option>
                <option value="4">4 - Very important</option>
                <option value="5">5 - Essential</option>
            </select>
            <div class="hint">Consider your customers' transportation needs</div>
        </div>

        <div class="question-group">
            <label>How important is the area's demographic match to your target market? (1-5)</label>
            <select name="q4" required>
                <option value="">Select importance...</option>
                <option value="1">1 - Not important</option>
                <option value="2">2 - Slightly important</option>
                <option value="3">3 - Moderately important</option>
                <option value="4">4 - Very important</option>
                <option value="5">5 - Essential</option>
            </select>
            <div class="hint">Consider income levels, age groups, and lifestyle patterns</div>
        </div>

        <div class="question-group">
            <label>What's your budget sensitivity to rent/property costs? (1-5)</label>
            <select name="q5" required>
                <option value="">Select sensitivity...</option>
                <option value="1">1 - Very flexible budget</option>
                <option value="2">2 - Somewhat flexible</option>
                <option value="3">3 - Moderate constraints</option>
                <option value="4">4 - Budget conscious</option>
                <option value="5">5 - Strictly limited</option>
            </select>
            <div class="hint">Higher numbers indicate more budget sensitivity</div>
        </div>

        <div class="question-group">
            <label>Please describe your business concept:</label>
            <textarea name="free_response" placeholder="Describe your business type, target market, operating hours, and any specific requirements or preferences..." required></textarea>
            <div class="hint">Include details about your business model, expected customer flow, and special requirements</div>
        </div>

        <button type="submit">Analyze Location Potential</button>
    </form>
</div>
</body>
</html>
'''

LOADING_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Loading</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; background: #f5f7fa; }
        .loader { text-align: center; }
        .spinner { border: 8px solid #f3f3f3; border-radius: 50%; border-top: 8px solid #3498db; width: 60px; height: 60px; animation: spin 1s linear infinite; margin: 20px auto; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body>
    <div class="loader">
        <div class="spinner"></div>
        <h2>Processing Data...</h2>
    </div>
    <script>
        const params = new URLSearchParams(window.location.search);
        const nextStep = params.get('next') || 'map';
        
        if (nextStep === 'map') {
            window.location.href = '/map';
        } else {
            fetch("/analyze_survey").then(r => r.json()).then(d => {
                window.location.href = d.redirect || '/map';
            }).catch(e => console.error(e));
        }
    </script>
</body>
</html>
'''

MAP_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Location Selection</title>
    <style>
        body { margin: 0; padding: 0; height: 100vh; font-family: Arial, sans-serif; }
        .search-container { position: fixed; top: 20px; left: 50%; transform: translateX(-50%); z-index: 1000; display: flex; gap: 10px; }
        #searchInput { width: 400px; padding: 12px; border: 1px solid #ddd; border-radius: 5px; font-size: 16px; }
        #map { height: 100%; width: 100%; }
        #analyzeBtn { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); padding: 15px 30px; 
                     background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
        .loading { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; 
                  background: rgba(255,255,255,0.8); justify-content: center; align-items: center; }
        #result { display: none; position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%); 
                 background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 6px rgba(0,0,0,0.1);
                 max-height: 400px; width: 80%; overflow-y: auto; }
    </style>
</head>
<body>
    <div class="search-container">
        <input id="searchInput" type="text" placeholder="Enter address or zip code...">
    </div>
    <div id="map"></div>
    <button id="analyzeBtn">Analyze Location</button>
    <div id="result"></div>
    <div class="loading">
        <div style="text-align: center;">
            <div class="spinner"></div>
            <h3>Analyzing location...</h3>
        </div>
    </div>
    <script>
        let map, marker;
        
        function initMap() {
            const defaultLocation = {lat: 40.7128, lng: -74.0060};
            map = new google.maps.Map(document.getElementById("map"), {
                zoom: 12,
                center: defaultLocation
            });
            
            marker = new google.maps.Marker({
                map: map,
                animation: google.maps.Animation.DROP
            });
            
            const searchInput = document.getElementById("searchInput");
            const autocomplete = new google.maps.places.Autocomplete(searchInput);
            
            autocomplete.addListener("place_changed", () => {
                const place = autocomplete.getPlace();
                if (!place.geometry) return;
                
                if (place.geometry.viewport) {
                    map.fitBounds(place.geometry.viewport);
                } else {
                    map.setCenter(place.geometry.location);
                    map.setZoom(17);
                }
                
                marker.setPosition(place.geometry.location);
            });
            
            document.getElementById("analyzeBtn").addEventListener("click", async () => {
                const center = marker.getPosition() || map.getCenter();
                document.querySelector(".loading").style.display = "flex";
                
                try {
                    const response = await fetch("/analyze_location", {
                        method: "POST",
                        headers: {"Content-Type": "application/json"},
                        body: JSON.stringify({lat: center.lat(), lng: center.lng()})
                    });
                    
                    const data = await response.json();
                    if (data.error) throw new Error(data.error);
                    
                    window.location.href = "/results";
                } catch (error) {
                    alert("Error analyzing location: " + error.message);
                } finally {
                    document.querySelector(".loading").style.display = "none";
                }
            });
        }
    </script>
    <script async defer src="https://maps.googleapis.com/maps/api/js?key={{ api_key }}&libraries=places&callback=initMap"></script>
</body>
</html>
'''

@app.route('/')
def survey():
    return SURVEY_HTML

@app.route('/submit_survey', methods=["POST"])
def submit_survey():
    data_file = get_data_file_path()
    if not os.path.exists(data_file):
        open(data_file, 'w').close()
    
    # Define questions with their full text
    questions = {
        "q1": {
            "text": "How important is foot traffic to your business?",
            "options": {
                "1": "Not important",
                "2": "Slightly important",
                "3": "Moderately important",
                "4": "Very important",
                "5": "Extremely important"
            }
        },
        "q2": {
            "text": "What's your priority level for being near complementary businesses?",
            "options": {
                "1": "Not a priority",
                "2": "Low priority",
                "3": "Medium priority",
                "4": "High priority",
                "5": "Essential priority"
            }
        },
        "q3": {
            "text": "How important is parking availability?",
            "options": {
                "1": "Not important",
                "2": "Slightly important",
                "3": "Moderately important",
                "4": "Very important",
                "5": "Essential"
            }
        },
        "q4": {
            "text": "How important is the area's demographic match to your target market?",
            "options": {
                "1": "Not important",
                "2": "Slightly important",
                "3": "Moderately important",
                "4": "Very important",
                "5": "Essential"
            }
        },
        "q5": {
            "text": "What's your budget sensitivity to rent/property costs?",
            "options": {
                "1": "Very flexible budget",
                "2": "Somewhat flexible",
                "3": "Moderate constraints",
                "4": "Budget conscious",
                "5": "Strictly limited"
            }
        }
    }
    
    # Process survey responses with full text
    formatted_responses = {}
    for q_id, q_info in questions.items():
        value = request.form.get(q_id, "")
        if value:
            formatted_responses[q_id] = {
                "question": q_info["text"],
                "response_value": value,
                "response_text": q_info["options"].get(value, "N/A")
            }
    
    # Add business description
    formatted_responses["business_description"] = request.form.get("free_response", "")
    
    # Store formatted responses
    with open(data_file, "a", encoding='utf-8') as f:
        f.write("\nSurvey Data:\n")
        f.write(json.dumps(formatted_responses, indent=2))
        f.write("\n")
    
    global_survey_data["survey"] = formatted_responses
    return redirect(url_for('loading', next='map'))

@app.route('/loading')
def loading():
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    if lat and lng:
        global_survey_data["coordinates"] = {"lat": float(lat), "lng": float(lng)}
    return LOADING_HTML

@app.route('/analyze_survey')
def analyze_survey():
    coords = global_survey_data.get("coordinates", {})
    if not coords:
        return jsonify({"error": "No coordinates provided"}), 400
    
    location_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    data_payload = get_enhanced_location_data(coords["lat"], coords["lng"], location_id)
    data_payload["survey_data"] = global_survey_data.get("survey", {})
    
    analysis = analyze_with_assistant(data_payload)
    store_analysis_data(coords["lat"], coords["lng"], data_payload, analysis)
    global_survey_data["score"] = get_location_score(analysis)
    
    return jsonify({"status": "ok", "redirect": "/results"})

@app.route('/map')
def map_page():
    return render_template_string(MAP_HTML, api_key=os.getenv("GOOGLE_API_KEY"))

@app.route('/get_score')
def get_score():
    score = global_survey_data.get("score","N/A")
    return jsonify({"score":score})

@app.route('/export_pdf')
def export_pdf():
    try:
        # Get the latest analysis
        analysis = get_last_analysis()
        if not analysis:
            return "No analysis available", 404
            
        latest = analysis[-1]
        
        pdf = FPDF()
        pdf.add_page()
        
        # Use standard font and size consistently
        pdf.set_font("Arial", size=12)
        
        # Add title
        pdf.cell(200, 10, txt="Location Analysis Report", ln=True, align='C')
        pdf.cell(200, 10, txt="", ln=True)  # Add spacing
        
        # Add score
        score = global_survey_data.get("score", "N/A")
        pdf.cell(200, 10, txt=f"Location Score: {score}/100", ln=True)
        pdf.cell(200, 10, txt="", ln=True)  # Add spacing
        
        # Format the analysis text for PDF
        analysis_text = latest["analysis"]
        
        # Split text into lines that fit the page width
        lines = []
        words = analysis_text.split()
        current_line = ""
        
        for word in words:
            test_line = current_line + " " + word if current_line else word
            if pdf.get_string_width(test_line) < 180:  # Leave margin
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        # Add each line to PDF
        for line in lines:
            pdf.cell(200, 10, txt=line.strip(), ln=True, align='L')
        
        # Create response
        response = make_response(pdf.output(dest='S'))
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename="location_analysis.pdf"'
        return response
        
    except Exception as e:
        console.print(f"[red]Error generating PDF: {str(e)}[/red]")
        return f"Error generating PDF: {str(e)}", 500

@app.route('/results')
def results_main():
    analysis = get_last_analysis()
    if not analysis:
        return "No analysis available", 404

    latest = analysis[-1]
    return render_template_string(
        RESULTS_HTML,
        score=global_survey_data.get("score", "N/A"),
        analysis=latest["analysis"]
    )


@app.route('/analyze_location', methods=["POST"])
def analyze_location():
    try:
        data = request.get_json()
        lat, lng = data["lat"], data["lng"]
        location_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        console.print("[yellow]Getting location data...[/yellow]")
        data_payload = get_enhanced_location_data(lat, lng, location_id)
        
        console.print("[yellow]Storing initial analysis data...[/yellow]")
        store_analysis_data(lat, lng, data_payload, "Analysis in progress...")
        
        console.print("[yellow]Starting complete location analysis...[/yellow]")
        analysis = analyze_with_assistant(data_payload)
        
        console.print("[green]Storing final analysis...[/green]")
        store_analysis_data(lat, lng, data_payload, analysis)
        
        global_survey_data["score"] = get_location_score(analysis)
        return jsonify({"status": "success", "analysis": analysis, "score": global_survey_data["score"]})
    except Exception as e:
        console.print(f"[red]Error in analysis: {str(e)}[/red]")
        return jsonify({"error": str(e)}), 500

global_survey_data = {"survey":{}, "score":"N/A"}

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

@app.route('/old_map')
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
    return sorted([b for b in businesses if b.get('rating') and b.get('reviews')], key=lambda x: (x['rating'] * math.log(x['reviews'] + 1)), reverse=True)[:limit]

def generate_and_save_street_views(businesses, location_id):
    """Generate and save street view images for top businesses"""
    urls = []
    
    # Create base pictures directory if it doesn't exist
    base_pictures_dir = Path(BASE_DIR) / "pictures"
    try:
        base_pictures_dir.mkdir(exist_ok=True)
    except Exception as e:
        print(f"Error creating base pictures directory: {e}")
        # Fallback to temp directory if base directory creation fails
        base_pictures_dir = Path(os.getenv('TEMP', '/tmp'))

    # Create location-specific directory
    image_dir = base_pictures_dir / f"location_{location_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    try:
        image_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating image directory: {e}")
        return [], str(base_pictures_dir)

    top_businesses = get_top_businesses(businesses)
    images_per_business = 2
    total_images = 0
    
    for idx, business in enumerate(top_businesses):
        if total_images >= 10:
            break
            
        lat = business.get("geometry", {}).get("location", {}).get("lat")
        lng = business.get("geometry", {}).get("location", {}).get("lng")
        name = business.get("name", "unknown")
        
        if not lat or not lng:
            continue
            
        # Create sanitized business name for folder
        safe_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
        safe_name = safe_name.replace(' ', '_')
        
        for angle in range(images_per_business):
            if total_images >= 10:
                break
                
            heading = angle * 180
            url = f"https://maps.googleapis.com/maps/api/streetview?size=600x400&location={lat},{lng}&heading={heading}&key={os.getenv('GOOGLE_API_KEY')}"
            urls.append({
                'url': url,
                'business_name': name,
                'rating': business.get('rating', 'N/A'),
                'reviews': business.get('reviews', 0)
            })
            
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    image_path = image_dir / f"{safe_name}_{angle}.jpg"
                    with open(image_path, 'wb') as f:
                        shutil.copyfileobj(response.raw, f)
                    total_images += 1
            except Exception as e:
                print(f"Error saving image for {name}: {e}")
                continue
    
    return urls, str(image_dir)

def get_data_file_path():
    return os.path.join(BASE_DIR, "data.txt")

def clean_business_for_storage(business):
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
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_data = {
        "location": data_payload.get("location", {}),
        "metrics": data_payload.get("metrics", {}),
        "businesses": [clean_business_for_storage(b) for b in data_payload.get("businesses", [])],
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
    business_types = [
        "establishment", "store", "restaurant", "food", "doctor", "bank",
        "shopping_mall", "pharmacy", "health", "beauty_salon", "cafe", "gym"
    ]
    seen_places = set()
    combined_places = []
    for btype in business_types:
        try:
            places_result = gmaps.places_nearby(location=(lat, lng), rank_by="distance", type=btype)
            for place in places_result.get("results", []):
                if place['place_id'] not in seen_places and len(combined_places) < 75:
                    combined_places.append(place)
                    seen_places.add(place['place_id'])
                if len(combined_places) >= 75:
                    break
            if len(combined_places) >= 75:
                break
        except Exception as e:
            print(f"Error fetching {btype} places: {str(e)}")
    businesses = []
    total_foot_traffic = 0
    
    headers = {
        "Accept": "application/json",
        "Authorization": os.getenv("FOOT_SQUARE_API_KEY")
    }
    
    try:
        fs_url = f"https://api.foursquare.com/v3/places/nearby?ll={lat},{lng}&radius=1000&limit=50"
        response = requests.get(fs_url, headers=headers)
        fs_data = response.json()
        
        # Calculate foot traffic based on venue popularity
        venues = fs_data.get('results', [])
        if venues:
            total_popularity = sum(venue.get('popularity', 50) for venue in venues)
            walking_volume = int((total_popularity / len(venues)) * 100)
        else:
            walking_volume = 5000  # fallback value
    except Exception as e:
        console.print(f"[red]Error fetching Foursquare data: {e}[/red]")
        walking_volume = 5000  # fallback value
    
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
            base_traffic = random.randint(100, 1000)
            rating_multiplier = float(place_details.get('rating', 3)) / 5
            distance_factor = 1 / (1 + distance)
            foot_traffic = int(base_traffic * rating_multiplier * distance_factor)
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
                "phone": place_details.get("formatted_phone_number") or ""
            })
        except Exception as e:
            print(f"Error processing place {place.get('name')}: {str(e)}")
    businesses.sort(key=lambda x: x.get('distance', float('inf')))
    street_view_businesses = [{**b, "geometry": {"location": gmaps.place(place['place_id'], fields=["geometry/location"])['result']["geometry"]["location"]}} for place,b in zip(combined_places[:50], businesses[:50])]
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
            "success_index": round(min(100, ((total_foot_traffic / (len(businesses) or 1)) / 100 * 0.4 + (5 - (sum(b['distance'] for b in businesses) / len(businesses) if businesses else 0)) * 10 * 0.3 + ((sum(b['rating'] for b in businesses if b.get('rating')) / len(businesses) if businesses else 0) * 10) * 0.3)), 2),
            "daily_walking_volume": walking_volume,
            "peak_hours_traffic": int(walking_volume * 0.2),
            "visual_coverage": "10 panoramic views of top-rated businesses",
            "total_searched_types": len(business_types),
            "total_unique_places_found": len(seen_places)
        }
    }

def analyze_with_assistant(data_payload):
    try:
        console.print("\n[bold blue]Starting Analysis Process[/bold blue]")
        console.print(Panel("[yellow]Creating new thread...[/yellow]"))
        thread = client.beta.threads.create()
        console.print(f"[green]Thread created: {thread.id}[/green]")
        
        # Wait for location data to be processed
        time.sleep(2)  # Give time for data.txt to be updated
        
        data_file = get_data_file_path()
        if os.path.exists(data_file):
            with open(data_file, 'r', encoding='utf-8') as f:
                historical_data = f.read()
                if historical_data.strip():
                    console.print("\n[bold yellow]Sending Complete Analysis Data:[/bold yellow]")
                    console.print(Panel(historical_data, title="Complete Analysis Data"))
                    
                    # Send the complete data including location analysis
                    context_msg = client.beta.threads.messages.create(
                        thread_id=thread.id,
                        role="user",
                        content=f"Complete Analysis Data:\n\n{historical_data}\n\nPlease analyze this location based on all available data including the survey responses, location metrics, and nearby businesses."
                    )
                    console.print(f"[green]Complete data message added: {context_msg.id}[/green]")
                    
                    # No need to send survey data separately as it's included in historical_data
                    current_analysis = "Please provide a detailed analysis and location score based on all the data provided above."
        else:
            # Fallback if no data file exists
            survey_info = data_payload.get("survey_data", {})
            current_analysis = f"Survey Data Only:\n{json.dumps(survey_info, indent=2)}\nPlease analyze based on available survey data."
        
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=current_analysis
        )
        
        console.print("\n[bold blue]Starting Assistant Run[/bold blue]")
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=os.getenv("ASSISTANT_ID")
        )
        
        with console.status("[bold green]Waiting for analysis...") as status:
            while run.status not in ["completed", "failed"]:
                run = client.beta.threads.runs.retrieve(
                    thread_id=thread.id,
                    run_id=run.id
                )
                console.print(f"[yellow]Status: {run.status}[/yellow]")
                time.sleep(1)
        
        if run.status == "failed":
            error_msg = f"Analysis failed: {run.last_error}"
            console.print(f"[red]{error_msg}[/red]")
            return error_msg
        
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        for msg in messages.data:
            if msg.role == "assistant":
                response = msg.content[0].text.value
                console.print("\n[bold green]Analysis Complete![/bold green]")
                console.print(Panel(response[:200] + "...", title="Preview of Analysis"))
                return response
        
        return "No response from assistant"
        
    except Exception as e:
        error_msg = f"Analysis Error: {str(e)}"
        console.print(f"[red]{error_msg}[/red]")
        return error_msg

RESULTS_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Location Analysis Results</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            background: #f5f7fa;
            color: #2d3748;
            line-height: 1.6;
        }
        .container {
            max-width: 1000px;
            margin: 40px auto;
            padding: 20px;
        }
        .header {
            text-align: center;
            margin-bottom: 40px;
        }
        .score-card {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
            margin-bottom: 30px;
            text-align: center;
        }
        .score {
            font-size: 48px;
            font-weight: 600;
            color: #4299e1;
            margin: 10px 0;
        }
        .score-label {
            font-size: 18px;
            color: #718096;
        }
        .analysis-section {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        }
        .analysis-content {
            white-space: pre-wrap;
            font-size: 16px;
            color: #4a5568;
        }
        .export-btn {
            display: inline-block;
            margin-top: 30px;
            padding: 12px 24px;
            background: #4299e1;
            color: white;
            text-decoration: none;
            border-radius: 8px;
            font-weight: 600;
            transition: background 0.3s ease;
        }
        .export-btn:hover {
            background: #3182ce;
        }
        .section-title {
            font-size: 24px;
            font-weight: 600;
            margin-bottom: 20px;
            color: #2d3748;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Location Analysis Results</h1>
        </div>
        <div class="score-card">
            <div class="score-label">Location Score</div>
            <div class="score">{{ score }}/10</div>
        </div>
        <div class="analysis-section">
            <h2 class="section-title">Detailed Analysis</h2>
            <div class="analysis-content">{{ analysis }}</div>
        </div>
        <center>
            <a href="/export_pdf" class="export-btn">Export to PDF</a>
        </center>
    </div>
</body>
</html>
'''

@app.route('/results/alternative')
def results():
    analysis = get_last_analysis()
    if not analysis:
        return "No analysis available", 404
    
    latest = analysis[-1]
    return render_template_string(
        RESULTS_HTML,
        score=global_survey_data.get("score", "N/A"),
        analysis=latest["analysis"]
    )

def format_response(data_payload, analysis):
    return {"analysis": analysis}

def get_location_score(analysis_text):
    score = "N/A"
    import re
    found = re.search(r'\bscore\s*[:=]\s*(\d+)', analysis_text.lower())
    if found:
        score = found.group(1)
    return score

@app.route('/analyze', methods=["POST"])
def analyze():
    try:
        req = request.get_json()
        lat, lng = req["lat"], req["lng"]
        location_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        data_payload = get_enhanced_location_data(lat, lng, location_id)
        store_analysis_data(lat, lng, data_payload, "Analysis pending...")
        analysis = analyze_with_assistant(data_payload)
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