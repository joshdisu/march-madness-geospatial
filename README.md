# March Madness Tournament with Geospatial Visualisation

This project simulates a March Madness-style tournament of college basketball teams, incorporating geospatial data to visualise team locations and the tournament winner on an interactive map.

## Features
- Reads team location data from a CSV file
- Geocodes team locations using OpenStreetMap's Nominatim API
- Simulates tournament matches based on seed-based probabilities
- Visualises the winning team's location using Folium
- Opens the map in the default web browser

## Requirements
- Python 3.x
- `geopy` library (`pip install geopy`)
- `folium` library (`pip install folium`)

## Usage
1. Prepare your `teams_locations.csv` with team names and locations.
2. Run the script `tournament_geospatial.py`.
3. The script will geocode locations, simulate the tournament, and open a map showing the winner's location.

## Notes
- Geocoding may take some time due to API rate limits.
- Manual coordinate fixes are included for failed geocoding results.
