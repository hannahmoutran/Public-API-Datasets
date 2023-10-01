import requests
import pandas as pd
import time
from datetime import datetime, timedelta
import os                                                                                                                                              
API_KEY = os.environ.get('NYT_API_KEY')                                                                                                                
if API_KEY:                                                                  
    print(f"The API key is: {API_KEY}")                                      
else:                                                                        
    print("The NYT_API_KEY environment variable is not set. Request one here: https://developer.nytimes.com/docs/books-product/1/overview") 

# Initialize an empty list to store all the data
all_data = []

URL = "https://api.nytimes.com/svc/books/v3/lists.json"

        
# Loop through the years
for year in range(2018, 2023):  # Update years as needed, this takes more than an hour
    # Initialize the start date to the first day of the year
    start_date = datetime(year, 1, 1)
    
    # Loop through the year week by week
    while start_date.year == year:
        # Convert start_date to string
        date_str = start_date.strftime('%Y-%m-%d')
        
        
        # API parameters
        params = {
            "api-key": API_KEY,
            "list": "picture-books",#change as needed
            "published_date": date_str
        }

        # Make the API request
        response = requests.get(URL, params=params)
        data = response.json()
        
        print(data)
        
        # Parse the data
        best_sellers = data.get('results', [])
        for book in best_sellers:
            all_data.append({
                'Title': book['book_details'][0]['title'],
                'Author': book['book_details'][0]['author'],
                'Contributor': book['book_details'][0]['contributor_note'],
                'Publisher': book['book_details'][0]['publisher'],
                'Rank': book['rank'],
                'Weeks on List': book['weeks_on_list'],
                'Date List Published': book['published_date'],
                'Year': year,
                'ISBN-13': book['book_details'][0]['primary_isbn13'], 
                'ISBN-10': book['book_details'][0]['primary_isbn10']
            })
        
        # Pause to respect rate limits (if applicable)
        time.sleep(20)  # Sleep for 20 seconds; adjust as needed
        
        # Increment start_date by 7 days to move to the next week
        start_date += timedelta(days=7)

# Convert all_data to a pandas DataFrame
df = pd.DataFrame(all_data)

# Save DataFrame to an Excel file
df.to_excel("NYTimes_Picture_Books_Best_Sellers.xlsx", index=False)
