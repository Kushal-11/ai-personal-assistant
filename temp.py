import requests

# The API's URL endpoint
url = 'https://www.eventbriteapi.com/v3/events/search/?token=7IOPF2YWYNKKC3QX34'

# Your API key
api_key = '7IOPF2YWYNKKC3QX34'

# Headers for authentication
headers = {
    'Authorization': f'Bearer {api_key}'
}

# Make a GET request to the API
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the response data (assuming it's in JSON format)
    data = response.json()
    print(data)
else:
    print(f'Error: {response.status_code}')