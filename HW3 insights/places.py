from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

api_key = os.getenv("GOOGLE_MAPS_API_KEY")

def fetch_locations_based_on_interests(interests):
    locations = []
    for interest in interests:
        endpoint = f"https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={interest}&inputtype=textquery&fields=photos,formatted_address,name,rating,opening_hours,geometry&key={api_key}"
        response = requests.get(endpoint)
        if response.status_code == 200:
            locations.extend(response.json()['candidates'])
        else:
            print(f"Failed to fetch locations for {interest}")
    return locations

@app.post("/fetch-locations/")
async def fetch_locations(interests: list):
    locations = fetch_locations_based_on_interests(interests)

    with open('static/locations.json', 'w') as f:
        json.dump(locations, f)
    return {"message": "Locations fetched and saved successfully."}

@app.get("/", response_class=HTMLResponse)
async def get_map_page():
    return FileResponse('index.html')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)