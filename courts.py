import requests
import csv
import time
import os
from typing import List, Dict, Any

GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

# Coordinates from https://tinyurl.com/suidar
locations = [
    (1.448065, 103.808533), (1.408855, 103.734970), (1.429104, 103.770676),
    (1.418250, 103.829271), (1.402442, 103.875811), (1.398666, 103.921817),
    (1.364635, 103.712674), (1.370001, 103.757378), (1.369041, 103.841400),
    (1.361941, 103.888858), (1.357822, 103.936580), (1.369149, 103.980182),
    (1.331685, 103.677998), (1.327909, 103.727093), (1.327175, 103.766966),
    (1.330608, 103.807211), (1.327862, 103.852873), (1.324872, 103.900874),
    (1.309351, 103.940013), (1.328915, 103.975718), (1.284271, 103.787909),
    (1.288733, 103.829183), (1.289076, 103.876562), (1.248231, 103.823347),
    (1.401291, 103.786646), (1.454833, 103.849131),
]


def fetch_places(location: tuple) -> List[Dict[str, Any]]:
    """Fetch places from Google Maps API for a given location."""
    places = []
    session = requests.Session()
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location[0]},{location[1]}&radius=3000&keyword=basketball court&key={GOOGLE_MAPS_API_KEY}"

    while True:
        try:
            response = session.get(url)
            response.raise_for_status()
            data = response.json()
            places.extend(data.get('results', []))

            if 'next_page_token' not in data:
                break

            next_page_token = data['next_page_token']
            time.sleep(2)  # Sleep to wait for the next page to be ready
            url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key={GOOGLE_MAPS_API_KEY}"
        except requests.RequestException as e:
            print(f"Request failed: {e}")
            break
        except ValueError as e:
            print(f"JSON decoding failed: {e}")
            break

    return places


def save_to_csv(places: List[Dict[str, Any]], filename: str):
    """Save unique places to a CSV file."""
    unique_places = {place['place_id']: place for place in places}

    with open(filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Latitude", "Longitude", "Google Maps Link"])
        for place in unique_places.values():
            name = place['name']
            lat = place['geometry']['location']['lat']
            lng = place['geometry']['location']['lng']
            place_id = place['place_id']
            maps_link = f"https://www.google.com/maps/place/?q=place_id:{place_id}"
            writer.writerow([name, lat, lng, maps_link])


def main():
    """Main function to fetch and save basketball court locations."""
    all_places = []
    for location in locations:
        all_places.extend(fetch_places(location))

    save_to_csv(all_places, "basketball_courts.csv")
    print("Data successfully saved to basketball_courts.csv")


if __name__ == "__main__":
    main()
