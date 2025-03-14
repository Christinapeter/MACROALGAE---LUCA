#!/usr/bin/env python
# coding: utf-8

# MATCHING NAMES FOR THEIR RESPECTIVE COLOUR AND FILLING OUT THE DATA IN THE OTHER SHEET TO THE CORRESPONDING NAME

# In[ ]:


import pandas as pd

# File paths
macroalgae_xlsx = r"C:\Users\Christina Peters\Downloads\MACROALGAE.xlsx"
seaweeds_csv_in = r"C:\Users\Christina Peters\OneDrive\Desktop\NEW MACROALAGE NIGHT.csv"
seaweeds_csv_out = r"C:\Users\Christina Peters\OneDrive\Desktop\NEW MACROALAGE NIGHT.csv"

# 1. Read the Excel file containing species lists by color
df_macro = pd.read_excel(macroalgae_xlsx)

# 2. Read the CSV file with the 'macrospecies' column, specifying encoding if necessary
df_seaweeds = pd.read_csv(seaweeds_csv_in, encoding="latin1")

# 3. Build sets of species for quick lookup (strip whitespace and ensure strings)
red_set = set(df_macro['RED'].dropna().astype(str).str.strip())
green_set = set(df_macro['GREEN'].dropna().astype(str).str.strip())
brown_set = set(df_macro['BROWN'].dropna().astype(str).str.strip())

def determine_algae_colors(species_str):
    """
    If a cell contains multiple species (assumed comma-separated),
    determine which color groups they belong to (red, green, brown)
    based on the sets from the Excel file.
    Returns a comma-separated string of color names, for example:
    "red algae, brown algae"
    """
    if pd.isna(species_str) or species_str == "":
        return None
    
    # Split the string by comma and strip whitespace from each species name
    species_list = [s.strip() for s in species_str.split(",") if s.strip()]
    colors = []
    for sp in species_list:
        # Check each species against the color sets
        if sp in red_set:
            colors.append("red algae")
        if sp in green_set:
            colors.append("green algae")
        if sp in brown_set:
            colors.append("brown algae")
    # Remove duplicates while preserving order
    colors = list(dict.fromkeys(colors))
    if colors:
        return ", ".join(colors)
    else:
        return None

# 4. Create a new column 'AlgaeColor' by applying the function to the 'macrospecies' column
df_seaweeds['AlgaeColor'] = df_seaweeds['macrospecies'].apply(determine_algae_colors)

# 5. Save the updated DataFrame to a new CSV file without removing any original data
df_seaweeds.to_csv(seaweeds_csv_out, index=False)
print(f"Updated CSV saved to: {seaweeds_csv_out}")

