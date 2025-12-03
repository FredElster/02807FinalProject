import requests
import csv
import os
from dotenv import load_dotenv
import time
import json
from pathlib import Path

print("CWD:", os.getcwd())
print("Script dir:", Path(__file__).parent)
print(".env exists in CWD?", os.path.exists(".env"))


# Load environment variables from .env file
load_dotenv()

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

print("CLIENT_ID loaded:", bool(CLIENT_ID))
print("CLIENT_SECRET loaded:", bool(CLIENT_SECRET))

CSV_FILENAME = 'spotify_data.csv'

def init_csv():
    # Create CSV file with header if it does not exist
    if not os.path.isfile(CSV_FILENAME):
        with open(CSV_FILENAME, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['timestamp', 'track_name', 'artist_name', 'album_name', 'popularity'])
        print(f"Created new CSV file: {CSV_FILENAME}")

def append_tracks_to_csv(rows, filename=CSV_FILENAME):
    # Append rows of track data to CSV file
    with open(filename, mode='a', encoding='utf-8', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def get_token():
    # Function to get Spotify API token (placeholder implementation)
    auth = (CLIENT_ID, CLIENT_SECRET)
    r = requests.post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "client_credentials"},
        auth=auth,
        timeout=30
    )
    r.raise_for_status()
    return r.json()['access_token']

def spotify_get(url, token, params=None, max_retries=5):
    headers = {"Authorization": f"Bearer {token}"}
    last_response = None

    for attempt in range(max_retries):
        r = requests.get(url, headers=headers, params=params, timeout=30)
        last_response = r

        if r.status_code == 429:
            retry = int(r.headers.get("retry-after", "1"))
            time.sleep(retry)
            continue

        if r.status_code in (500, 502, 503, 504):
            time.sleep(2 ** attempt)
            continue

        r.raise_for_status()
        return r.json()
    
    if last_response is not None:
        last_response.raise_for_status()
    raise Exception("Failed to get a valid response from Spotify API after retries.")

def get_genre_seeds(token):
    url = "https://api.spotify.com/v1/recommendations/available-genre-seeds"
    return spotify_get(url, token)

def get_categories(token, limit=50):
    url = "https://api.spotify.com/v1/browse/categories"
    return spotify_get(url, token, params={"limit": limit})

def get_category_playlists(category_id, token, limit=50):
    url = f"https://api.spotify.com/v1/browse/categories/{category_id}/playlists"
    return spotify_get(url, token, params={"limit": limit})

def search_playlists(keyword, token, limit=50):
    url = "https://api.spotify.com/v1/search"
    return spotify_get(url, token, params={"q": keyword, "type": "playlist", "limit": limit})

def scrape_genre(genre_keyword, token, playlist_limit=20):
    # Search public playlists by a given genre keyword
    # fetch all tracks for each playlist found
    # return list of track data rows via save_callback
    print(f"Scraping genre: '{genre_keyword}' ===")
    try:
        search_results = search_playlists(genre_keyword, token, limit=playlist_limit)
        playlist_items = search_results.get('playlists', {}).get('items', [])

        if not playlist_items:
            print(f"No playlists found for genre '{genre_keyword}'")
            return
        
        for idx, p in enumerate(playlist_items, start=1):
            if p is None:
                print(f"Skipping playlist #{idx} due to None value")
                continue
        
            playlist_id = p.get("id")
            playlist_name = p.get("name")
            track_info = p.get("tracks") or {}
            total_tracks = track_info.get("total")

            if not playlist_id:
                print(f"Skipping playlist #{idx} due to missing ID")
                continue
            print(f"Playlist: {playlist_id} - {playlist_name} ({total_tracks} tracks)")

            # Fetch all tracks in the playlist
            tracks = get_playlist_tracks(playlist_id, token)
            print(" -> tracks fetched:", len(tracks))

            # Build CSV rows
            rows = []
            for t in tracks:
                track = t.get("track")
                if track is None:
                    continue
                
                track_id = track.get("id")
                track_name = track.get("name")
                artists = ", ". join(a["name"] for a in track.get("artists", []))

                rows.append([
                    genre_keyword,
                    track_id,
                    playlist_name,
                    track_id,
                    track_name,
                    artists,
                ])

            # Append to CSV
            append_tracks_to_csv(rows)

    except requests.HTTPError as e:
        print(f"HTTP error occurred while scraping genre '{genre_keyword}': {e}")

def get_playlist_tracks(playlist_id, token):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    items = []
    params = {"limit": 100, "offset": 0}
    while True:
        data = spotify_get(url, token, params=params)
        items.extend(data.get("items", []))

        next_url = data.get("next")
        if next_url:
            url = next_url
            params = None  # next_url already contains all params
        else:
            break
    return items

if __name__ == "__main__":
    init_csv()
    token = get_token()

    # Try genre seeds retrieval with error handling
    try:
        seeds = get_genre_seeds(token).get("genres", [])
        print("Genres (seed list):", seeds[30])
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            print("Genre seeds endpoint not found (404). Skipping genre seed retrieval.")
        else:
            raise

    # Get categories, just to see if it works
    cats = get_categories(token)
    print("\nFirst 20 categories:")
    for c in cats.get("categories", {}).get("items", [])[:20]:
        print("cateogories:", c["id"], "-", c["name"])

    # Define list of genres to scrape
    genres_to_scrape = [
        "rock",
        "pop",
        "hip hop",
        "metal",
        "jazz",
        "classical",
        "country",
        "electronic",
        "r&b",
        "indie",
        "folk",
        "blues",
        "reggae",
        "punk",
        "soul",
        "latin",
        "k-pop",
    ]

    # Loop over all genres and scrape each one
    for genre in genres_to_scrape:
        scrape_genre(genre, token, playlist_limit=50)

    print("\nDone datascraping all genres.")