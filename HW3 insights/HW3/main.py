from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
import os
import requests
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
OPENWEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def generate_recommendations(places_data):
    recommendations = []
    if not places_data['candidates']:
        recommendations.append("No places found for your interest. Try something else!")
    else:
        for place in places_data['candidates']:
            if place.get('rating', 0) > 4.5:
                recommendations.append(f"Highly recommended: {place['name']} - Excellent ratings!")
            else:
                recommendations.append(f"Recommended: {place['name']} - Good place to visit.")
    return recommendations

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/get-locations", response_class=HTMLResponse)
async def get_locations(request: Request, interest: str = Form(...)):
    # Fetch places from Google Places API
    google_places_url = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={interest}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={GOOGLE_API_KEY}"
    places_response = requests.get(google_places_url).json()

    recommendations = generate_recommendations(places_response)

    locations = [{
        "name": place['name'],
        "lat": place['geometry']['location']['lat'],
        "lng": place['geometry']['location']['lng']
    } for place in places_response.get('candidates', [])]


    # Return the template response with locations and recommendations
    return templates.TemplateResponse("index.html", {
        "request": request,
        "recommendations": recommendations,
        "locations": locations
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.5", port=8000)
