import csv
from dataclasses import dataclass
import random 
from geopy.geocoders import Nominatim
import time

@dataclass
class Team:
    name: str
    seed: int
    latitude: float = None
    longitude: float = None

# Read team locations from CSV 

team_locations = {}
with open(r"C:\Users\joshu\OneDrive\Desktop\Python projects\datasets\teams_locations.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        team_locations[row['team_name']] = row['location']

# Geocode locations

def robust_geocode(geolocator, location, tries=3, delay=2):
    for i in range(tries):
        try:
            loc = geolocator.geocode(location, timeout=10)
            if loc:
                return loc
        except Exception as e:
            print(f"Attempt {i+1} failed for {location}: {e}")
        time.sleep(delay)
    return None

geolocator = Nominatim(user_agent="tournament_geocoder")
location_coords = {}

for team, location in team_locations.items():
    loc = robust_geocode(geolocator, location)
    if loc:
        location_coords[team] = (loc.latitude, loc.longitude)
    else:
        print(f"Could not geocode: {team} ({location})")
        location_coords[team] = (None, None)

# Manual fallback for teams that failed
location_coords["Alabama ST/Saint Francis U"] = (32.3668, -86.2999)
location_coords["San Diego St/North Carolina"] = (32.7157, -117.1611)
location_coords["Oklahoma"] = (35.2226, -97.4395)
location_coords["Kentucky"] = (38.0406, -84.5037)
location_coords["UCLA"] = (34.0689, -118.4452)

time.sleep(2)  # To avoid hitting the API too fast

#Create Team with coordinates

def get_team(name, seed):
    lat, lon = location_coords.get(name, (None, None))
    return Team(name, seed, lat, lon)


first_round = [
    # SOUTH
    (get_team("Auburn", 1), get_team("Alabama ST/Saint Francis U", 16)),
    (get_team("Louisville", 8), get_team("Creighton", 9)),
    (get_team("Michigan", 5), get_team("UC San Diego", 12)),
    (get_team("Texas A&M", 4), get_team("Yale", 13)),
    (get_team("Ole Miss", 6), get_team("San Diego St/North Carolina", 11)),
    (get_team("Iowa St.", 3), get_team("Lipscomb", 14)),
    (get_team("Marquette", 7), get_team("New Mexico", 10)),
    (get_team("Michigan St.", 2), get_team("Bryant", 15)),
    # WEST
    (get_team("Florida", 1), get_team("Norfolk St.", 16)),
    (get_team("UConn", 8), get_team("Oklahoma", 9)),
    (get_team("Memphis", 5), get_team("Colorado St.", 12)),
    (get_team("Maryland", 4), get_team("Grand Canyon", 13)),
    (get_team("Missouri", 6), get_team("Drake", 11)),
    (get_team("Texas Tech", 3), get_team("UNC Wilmington", 14)),
    (get_team("Kansas", 7), get_team("Arkansas", 10)),
    (get_team("St. John's", 2), get_team("Omaha", 15)),
    # EAST
    (get_team("Duke", 1), get_team("America/Mount St Mary's", 16)),
    (get_team("Mississippi St.", 8), get_team("Baylor", 9)),
    (get_team("Oregon", 5), get_team("Liberty", 12)),
    (get_team("Arizona", 4), get_team("Akron", 13)),
    (get_team("BYU", 6), get_team("VCU", 11)),
    (get_team("Wisconsin", 3), get_team("Montana", 14)),
    (get_team("Saint Mary's", 7), get_team("Vanderbilt", 10)),
    (get_team("Alabama", 2), get_team("Robert Morris", 15)),
    # MIDWEST
    (get_team("Houston", 1), get_team("SIU Edwardsville", 16)),
    (get_team("Gonzaga", 8), get_team("Georgia", 9)),
    (get_team("Clemson", 5), get_team("McNeese", 12)),
    (get_team("Purdue", 4), get_team("High Point", 13)),
    (get_team("Illinois", 6), get_team("Texas/Xavier", 11)),
    (get_team("Kentucky", 3), get_team("Troy", 14)),
    (get_team("UCLA", 7), get_team("Utah St.", 10)),
    (get_team("Tennessee", 2), get_team("Wofford", 15)),
]


def simulate_game(team1, team2):
    team1_seed_weight = 1 / (team1.seed)
    team2_seed_weight = 1 / (team2.seed)

    # Uncomment the following lines to use a power for seed weighting (higher power means more weight to better seeds)
    # power = 1.1618
    # team1_seed_weight = 1 / (team1.seed**power)
    # team2_seed_weight = 1 / (team2.seed**power)

    # Convert to probabilities
    total = team1_seed_weight + team2_seed_weight
    team1_prob = 100 * (team1_seed_weight / total)
    team2_prob = 100 * (team2_seed_weight / total)

    # Get winner based on probabilities
    winner = random.choices([team1, team2], weights=[team1_prob, team2_prob], k=1)[0]

    print(
        f"{team1.name}-{team1.seed} ({team1_prob:.1f}%) vs {team2.name}-{team2.seed} ({team2_prob:.1f}%), Winner: {winner.name}",
    )

    return winner


def simulate_tournament(first_round):
    current_games = first_round
    while len(current_games) > 0:
        print("\n===== NEW ROUND =====")
        winners = []

        for team1, team2 in current_games:
            winner = simulate_game(team1, team2)
            winners.append(winner)
        
        if len(winners) == 1:
            return winners[0]
        
        next_round = []
        for i in range(0, len(winners), 2):
            next_round.append((winners[i], winners[i + 1]))

        current_games = next_round
    return None


import folium
import webbrowser
import os

import folium
import webbrowser
import os

def plot_winner(team):
    if team.latitude is not None and team.longitude is not None:
        m = folium.Map(location=[team.latitude, team.longitude], zoom_start=6)
        folium.Marker([team.latitude, team.longitude], popup=team.name).add_to(m)
        save_path = r"C:\Users\joshu\OneDrive\Desktop\Python projects\winner_location.html"
        m.save(save_path)
        print(f"Winner location map saved as {save_path}")
        webbrowser.open('file://' + os.path.realpath(save_path))
    else:
        print("No location data for winner.")

winner = simulate_tournament(first_round)
print(f"{winner.name} wins the tournament!")
plot_winner(winner)