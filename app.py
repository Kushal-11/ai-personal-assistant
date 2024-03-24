from fastapi import FastAPI, HTTPException, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import httpx
from dotenv import load_dotenv
import os

from fastapi.middleware.cors import CORSMiddleware
from typing import List
from pydantic import BaseModel
import requests


# Load the .env file
load_dotenv()

# Access your API keys
weather_api_key = os.getenv('WEATHER_API_KEY')
news_api_key = os.getenv('NEWS_API_KEY')
maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


'''---------------------------------------------Finance--------------------------------------------------------------'''

# Finance data
class Transaction(BaseModel):
    date: str
    description: str
    amount: float
    category: str

class AccountBalance(BaseModel):
    account_type: str
    balance: float

class FinanceData(BaseModel):
    balances: List[AccountBalance]
    transactions: List[Transaction]

# Mock data for demonstration
mock_finance_data = FinanceData(
    balances=[
        {"account_type": "Checking", "balance": 1200.50},
        {"account_type": "Savings", "balance": 5600.75},
    ],
    transactions=[
        {"date": "2024-02-01", "description": "Grocery Store", "amount": -54.23, "category": "Food & Dining"},
        {"date": "2024-02-02", "description": "Monthly Salary", "amount": 3000, "category": "Income"},
    ]
)

'''-----------------------------------------------------------------------------------------------------------------'''



'''---------------------------------------------Fitness--------------------------------------------------------------'''
# Define your data model for the request body
class FitnessData(BaseModel):
    activity: str
    duration: int
    weight: int

# Function to calculate calories burned
def calculate_calories_burned(activity, duration, weight):

    MET_values = {"running": 10, "cycling": 8}  # MET values for activities
    calories_burned = (MET_values[activity] * 3.5 * weight / 2.2 / 60) * duration
    source = "Compendium of Physical Activities"
    return calories_burned, source

'''------------------------------------------------------------------------------------------------------------------'''

# app.mount("/static", StaticFiles(directory="Websites"), name="index.html")
app.mount("/static", StaticFiles(directory="Websites"), name="weather.html")
app.mount("/static", StaticFiles(directory="Websites"), name="finance.html")
app.mount("/static", StaticFiles(directory="Websites"), name="fitness.html")



@app.get("/", response_class=HTMLResponse)
async def root():
    with open('Websites/index.html', 'r') as f:
        html_content = f.read()
    return HTMLResponse(content=html_content, status_code=200)

@app.get("/map")
async def get_map(lat: float, lon: float, city: str):

    map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=12&size=400x400&markers=color:red%7Clabel:C%7C{lat},{lon}&key={maps_api_key}"

    response = requests.get(map_url)

    if response.status_code == 200:
        return response.content  # Directly return the image content
    else:
        raise HTTPException(status_code=400, detail="Error fetching map image")

@app.get("/weather")
async def get_weather(lat: float, lon: float):
    api_key = weather_api_key
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

    # 40.7128, -74.0060 is the latitude and longitude of New York City

    async with httpx.AsyncClient() as client:
        response = await client.get(weather_url)

        if response.status_code == 200:
            data = response.json()
            # Generate the map image URL
            map_url = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=12&size=400x400&markers=color:red%7Clabel:C%7C{lat},{lon}&key={maps_api_key}"
            weather = {
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "city": data["name"],
                "country": data["sys"]["country"],
                "map_url": map_url
            }
            return weather


        else:
            raise HTTPException(status_code=404, detail="Weather data not found")



class UserInterests(BaseModel):
    interests: list[str]

@app.post("/news")
async def get_news(user_interests: UserInterests):
    query = " OR ".join(user_interests.interests)  # Construct a query for the interests
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={news_api_key}"

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Error fetching news")
        return response.json()  # Return the JSON response directly to the client


@app.get("/schedules")
async def manage_schedules():
    return {"message": "Your plans for today"}


@app.get("/finances", response_model=FinanceData)
async def get_finances():
    return mock_finance_data



@app.put("/calculate-calories", response_class=JSONResponse)
async def calculate_calories(data: FitnessData):
    calories, source = calculate_calories_burned(data.activity, data.duration, data.weight)
    return {"calories": calories, "source": source}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
