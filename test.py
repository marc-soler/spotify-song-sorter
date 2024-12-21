# %%
import os
import pandas as pd
import numpy as np
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

# %%
scope = "user-library-read"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.environ["SPOTIFY_CLIENT_ID"],
        client_secret=os.environ["SPOTIFY_CLIENT_SECRET"],
        redirect_uri=os.environ["SPOTIFY_REDIRECT_URI"],
        scope=scope,
    )
)


# %%
def get_saved_tracks():
    results = []
    offset = 0
    while True:
        response = sp.current_user_saved_tracks(limit=50, offset=offset)
        results.extend(response["items"])
        offset += len(response["items"])
        if not response["next"]:
            break
    return results


saved_tracks = get_saved_tracks()

# %%
track_ids = []
track_metadata = []

for item in saved_tracks:
    track = item["track"]
    track_ids.append(track["id"])
    track_metadata.append(
        {
            "id": track["id"],
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "album": track["album"]["name"],
            "release_date": track["album"]["release_date"],
            "popularity": track["popularity"],
        }
    )

# %%
# Combine metadata and audio features
data = []
for meta, features in zip(track_metadata, audio_features):
    if features:  # Sometimes features may be None
        data.append(
            {
                **meta,
                "danceability": features["danceability"],
                "energy": features["energy"],
                "valence": features["valence"],
                "tempo": features["tempo"],
                "loudness": features["loudness"],
                "acousticness": features["acousticness"],
                "instrumentalness": features["instrumentalness"],
                "liveness": features["liveness"],
                "speechiness": features["speechiness"],
                "key": features["key"],
                "mode": features["mode"],
                "time_signature": features["time_signature"],
            }
        )

# Convert to pandas DataFrame
df = pd.DataFrame(track_metadata)

# Save to CSV or view the dataset
df.to_csv("spotify_saved_tracks.csv", index=False)
print(df.head())
