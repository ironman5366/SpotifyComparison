# Builtin imports
import json

# External imports
import requests

codes = json.load(open('codes.json', encoding="utf-8"))

person_one = "max"
person_two = "thomas"

code_one = codes[person_one]
code_two = codes[person_two]

track_data = {}


def get_user_tracks(code):
    """
    Get a users tracks from the API
    :param code: The auth code
    :return tracks: a list of tracks
    """
    auth_header = f"Bearer {code}"
    tracks = set()
    next_url = 'https://api.spotify.com/v1/me/tracks?limit=50'
    while next_url:
        print(next_url)
        res = requests.get(next_url, headers={
            "Authorization": auth_header
        })
        j = res.json()
        next_url = j['next']
        for item in j['items']:
            track = item['track']
            track_id = f"{track['name']} by {track['artists'][0]['name']}"
            if track_id not in track_data.keys():
                track_data[track_id] = track
            tracks.add(track_id)
    return tracks


one_tracks = get_user_tracks(code_one)
two_tracks = get_user_tracks(code_two)

combined_similarity = []

for track_id in one_tracks:
    if track_id in two_tracks:
        combined_similarity.append(track_data[track_id])

with open('simliarities.html', 'w') as similarity_file:
    similarity_file.write(f"<h1>{len(combined_similarity)} common tracks found</h1>\n")
    for track_info in combined_similarity:
        print(track_info['name'])
        similarity_file.write(f"<div>\n"
                              f"<h3><a href=\"{track_info['external_urls']['spotify']}\">{track_info['name']}</a> by "
                              f"{track_info['artists'][0]['name']}</h3>\n"
                              f"<img src=\"{track_info['album']['images'][0]['url']}\" width=100/>\n"
                              f"</div>\n")
