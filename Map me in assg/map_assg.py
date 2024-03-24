from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
import httpx
from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Access your API keys
weather_api_key = os.getenv('WEATHER_API_KEY')
maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():

    html_file_path = 'weather.html'
    with open(html_file_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/config")
async def get_config():
    return JSONResponse({"googleMapsApiKey": maps_api_key})

weather_icon_mapping = {
    "clear sky": "01d",  # Use '01n' for night
    "few clouds": "02d",
    "scattered clouds": "03d",
    "broken clouds": "04d",
    "shower rain": "09d",
    "rain": "10d",
    "thunderstorm": "11d",
    "snow": "13d",
    "mist": "50d",
    "overcast clouds": "04d"
}


@app.get("/weather")
async def get_weather(lat: float, lon: float):
    api_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}&units=metric"
    async with httpx.AsyncClient() as client:
        response = await client.get(api_url)
        if response.status_code == 200:
            data = response.json()

            weather_description = data["weather"][0]["description"]
            weather_icon = weather_icon_mapping.get(weather_description, "01d")  # Default to clear sky if not found

            return {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "city": data["name"],
                "icon": weather_icon
            }
        else:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch weather data")


