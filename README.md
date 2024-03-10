# AI Personal assistant

My vision is to create a personal assistant using AI that actually "knows you"!

It would provide curated recommendations for the user and will help to increase productivity in day-to-day life.

## Objective
My objective is to make use of various API services and integrate it in one platform so the user have all of his daily needs
on fingertips.

## API's used
1. Newsapi: For fetching new articles based on the user's interests
2. Openweatherapi: For getting the weather and providing insights to the user based on geolocation.


## Steps to install
### 1. Cloning the repository:
Assuming you have git installed on your local machine, clone this repository
```bash
git clone https://github.com/Kushal-11/ai-personal-assistant
cd ai-personal-assistant
```

### 2. Install required Python packages:
```bash
pip install -r requirements.txt
```
You can run the app using the following command
```bash
uvicorn app:app --host 127.0.0.5 --port 8000 --reload
```

## Features
### 1. News
It fetches news articles based on the user's interests, a valuable feature for users who want to stay updated on specific topics. It could also be used by businesses to keep track of news related to their industry or competitors.


### 2. Weather
Provides weather information based on the latitude and longitude provided. This could be useful for users who want to check the weather in their area or any other location. It could be particularly useful for businesses related to travel or outdoor activities.


### 3. Fitness
Here the number of calories burned based on the activity, duration, and weight provided are calculated. It is useful for users who are trying to maintain or lose weight. It could also be used by fitness or health-related businesses to provide personalized recommendations to their clients.

### 4. Finance
We display the financial data, including account balances and transactions of the user so it is useful for users who want to track their spending or income. For businesses, it could be used to monitor financial performance or cash flow.



## License
MIT License
