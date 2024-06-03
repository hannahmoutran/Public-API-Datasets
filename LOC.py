import requests
import pandas as pd
from datetime import datetime

def fetch_loc_data(query, from_year, to_year):
    base_url = "https://www.loc.gov/search/"
    items = []

    for year in range(from_year, to_year + 1):
        # Construct the API URL for each year
        params = {
            'q': query,
            'fo': 'json',
            'dates': f'{year}/{year}',  # Targeting specific years
            'c': 100,  # Number of results per page (can be adjusted based on rate limits)
            'sp': 1  # Starting from the first page
        }
        response = requests.get(base_url, params=params)
        data = response.json()
        
        # Check if results are found
        if 'results' in data:
            for item in data['results']:
                items.append({
                    'Title': item.get('title', 'No Title Available'),
                    'Date': item.get('date', 'No Date Available'),
                    'URL': item.get('id', 'No URL Available'),
                    'Description': item.get('description', ['No Description Available'])[0]
                })
                
        # Handle pagination if necessary (assuming up to 1000 items needed for simplicity)
        total_items = data.get('pagination', {}).get('of', 1)
        current_page = data.get('pagination', {}).get('current', 1)
        total_pages = (total_items // 100) + 1

        while current_page < total_pages:
            current_page += 1
            params['sp'] = current_page
            response = requests.get(base_url, params=params)
            data = response.json()
            for item in data['results']:
                items.append({
                    'Title': item.get('title', 'No Title Available'),
                    'Date': item.get('date', 'No Date Available'),
                    'URL': item.get('id', 'No URL Available'),
                    'Description': item.get('description', ['No Description Available'])[0]
                })

    return items

# Function to save the data to CSV
def save_to_csv(items, filename):
    df = pd.DataFrame(items)
    df.to_csv(filename, index=False)
    print(f'Data saved to {filename}')

# Define the search terms and date range
query_terms = "Artificial Intelligence"
from_year = 2023
to_year = 2024
filename = "AI__LoC_Resources.csv"

# Fetch the data
items = fetch_loc_data(query_terms, from_year, to_year)

# Save the data to a CSV file
save_to_csv(items, filename)
