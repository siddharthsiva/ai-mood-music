from utils.storage import load_json, save_json

COLLAB_FILE = "data/collab_playlists.json"

def create_shared_playlist(name, user):
    data = load_json(COLLAB_FILE)
    if name not in data:
        data[name] = {"owner": user, "contributors": [user], "tracks": []}
        save_json(COLLAB_FILE, data)

def join_shared_playlist(name, user):
    data = load_json(COLLAB_FILE)
    if name in data and user not in data[name]["contributors"]:
        data[name]["contributors"].append(user)
        save_json(COLLAB_FILE, data)

def add_track_to_shared(name, track, user):
    data = load_json(COLLAB_FILE)
    if name in data and user in data[name]["contributors"]:
        data[name]["tracks"].append(track)
        save_json(COLLAB_FILE, data)

def get_shared_tracks(name):
    data = load_json(COLLAB_FILE)
    return data.get(name, {}).get("tracks", [])
