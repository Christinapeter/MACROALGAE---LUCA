#!/usr/bin/env python
# coding: utf-8

# USING LATITUDE AND LONDITUDE TO GET COMPANY NAME , ADDRESS ETC

# In[ ]:


import pandas as pd
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

def get_company_name(geolocator, lat, lon, max_retries=3):
    """
    Reverse geocode the given latitude and longitude.
    Attempts to extract a 'name' from the namedetails, falling back to the full address.
    """
    retries = 0
    while retries < max_retries:
        try:
            # Request reverse geocoding with namedetails enabled
            location = geolocator.reverse((lat, lon), exactly_one=True, timeout=10, namedetails=True)
            if location:
                raw = location.raw or {}
                # Safely retrieve namedetails ensuring it's a dict before checking for 'name'
                namedetails = raw.get("namedetails")
                if namedetails and isinstance(namedetails, dict) and "name" in namedetails:
                    return namedetails["name"]
                else:
                    return location.address
            else:
                return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            print(f"Error: {e}. Retrying...")
            retries += 1
            time.sleep(2)
    return None

def process_csv(input_file, output_file):
    # Initialize Nominatim with a custom user agent
    geolocator = Nominatim(user_agent="company_locator")
    
    # Load the CSV file
    df = pd.read_csv(input_file)
    
    # Ensure that latitude and longitude columns exist
    if 'latitude' not in df.columns or 'longitude' not in df.columns:
        print("Input CSV must contain 'latitude' and 'longitude' columns")
        return
    
    # Add a new column for the company name (or reverse geocoded name)
    df['company_name'] = None

    # Iterate over each row in the DataFrame and perform reverse geocoding
    for index, row in df.iterrows():
        lat = row['latitude']
        lon = row['longitude']
        if pd.notnull(lat) and pd.notnull(lon):
            company = get_company_name(geolocator, lat, lon)
            df.at[index, 'company_name'] = company
            print(f"Row {index}: {company}")
            # Delay to avoid rate limiting
            time.sleep(1)
        else:
            print(f"Row {index}: Missing coordinates")
    
    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    input_file = r'C:\Users\Christina Peters\OneDrive\Desktop\Macroalgae.csv'
    output_file = r'C:\Users\Christina Peters\OneDrive\Desktop\Macroalgae_with_company.csv'
    process_csv(input_file, output_file)

