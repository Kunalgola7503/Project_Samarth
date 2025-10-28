import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

api_key = os.getenv("API_KEY")

url = f"https://api.data.gov.in/resource/35be999b-0208-4354-b557-f6ca9a5355de?api-key={api_key}&format=json"

response = requests.get(url)
data = response.json()

df = pd.json_normalize(data['records'])
print(" Data fetched successfully!\n")
print(df.head())

df.to_csv("crop_production_data.csv", index=False)
print("\n Data saved as 'crop_production_data.csv'")

