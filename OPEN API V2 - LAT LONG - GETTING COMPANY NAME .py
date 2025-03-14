#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import requests
import time

def get_osm_data_from_latlon(lat, lon):
    """
    Query OSM's reverse geocoding API using latitude and longitude.
    Returns a dictionary with the display name, address details,
    namedetails (which may include a company name), and an extracted company name.
    """
    base_url = "https://nominatim.openstreetmap.org/reverse"
    params = {
        'lat': lat,
        'lon': lon,
        'format': 'json',
        'addressdetails': 1,   # Get detailed address information
        'namedetails': 1       # Get extra name details if available
    }
    
    try:
        response = requests.get(base_url, params=params, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status()
        data = response.json()
        if data:
            display_name = data.get("display_name", "N/A")
            address = data.get("address", {})
            # Ensure namedetails is a dictionary even if it's None
            namedetails = data.get("namedetails") or {}
            # Try to extract a company name from namedetails if available
            company_name_osm = namedetails.get("name", "N/A")
            return {
                "display_name": display_name,
                "address": address,
                "namedetails": namedetails,
                "company_name_osm": company_name_osm
            }
        else:
            return {
                "display_name": "Not found",
                "address": {},
                "namedetails": {},
                "company_name_osm": "Not found"
            }
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for lat: {lat}, lon: {lon}: {e}")
        return {
            "display_name": "Error",
            "address": {},
            "namedetails": {},
            "company_name_osm": "Error"
        }

# Specify the path to your CSV file with latitude and longitude columns
csv_file = r"C:\Users\Christina Peters\OneDrive\Desktop\NEW MACROALAGE NIGHT.csv"

# Attempt to load the CSV file
try:
    df = pd.read_csv(csv_file)
    print("CSV loaded successfully. Here are the first few rows:")
    print(df.head())
except Exception as e:
    print("Error reading CSV file:", e)
    exit()

# Initialize lists for new columns
display_names = []
addresses = []
namedetails_list = []
company_names_osm = []

# Loop through each row and query OSM's reverse geocoding API
for index, row in df.iterrows():
    # Use get() to avoid KeyError if the column names are off
    lat = row.get('latitude')
    lon = row.get('longitude')
    
    if pd.isnull(lat) or pd.isnull(lon):
        print(f"Row {index} missing latitude or longitude. Skipping row.")
        display_names.append("Missing lat/lon")
        addresses.append({})
        namedetails_list.append({})
        company_names_osm.append("Missing lat/lon")
        continue

    print(f"Processing row {index} with lat: {lat}, lon: {lon}")
    osm_data = get_osm_data_from_latlon(lat, lon)
    print(f"Result for row {index}:", osm_data)
    
    display_names.append(osm_data["display_name"])
    addresses.append(osm_data["address"])
    namedetails_list.append(osm_data["namedetails"])
    company_names_osm.append(osm_data["company_name_osm"])
    
    # Pause to respect OSM API rate limits
    time.sleep(1)

# Add the new information as additional columns in the DataFrame
df['display_name_osm'] = display_names
df['address_osm'] = addresses
df['namedetails_osm'] = namedetails_list
df['company_name_osm'] = company_names_osm

# Save the updated DataFrame back to the same CSV file
df.to_csv(csv_file, index=False)
print(f"Data saved to {csv_file}")

