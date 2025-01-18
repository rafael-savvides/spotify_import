# Import a list of albums or artists into a Spotify playlist.
# For help, run python [this_file].py --help.

import argparse
import datetime
from pathlib import Path

from .bandcamp import scrape_album_names
from .client import add_to_playlist, create_playlist, make_spotify_client
from .io import read_albums, read_artists, read_tracks, save_tracks
from .search import albums_to_track_ids, artists_to_track_ids


def import_to_playlist(
    file_in: str,
    mode: str,
    name: str,
    id: int,
    auth: dict,
    file_out: str = None,
    min_sim_artist: float = 60,
    min_sim_album: float = 60,
):
    """Import to Spotify playlist

    Args:
        file_in (str): Input file.
        mode (str): Type of file_in. One of albums, artists, tracks.
        name (str): Name of new Spotify playlist.
        id (int): ID of existing Spotify playlist.
        auth (dict): Authentication information: client_id, client_secret, redirect_uri, client_id.
        file_out (str, optional): Output file. Defaults to None.
    """
    file_out = file_out if file_out else f"{file_in}_track_ids.txt"

    client = make_spotify_client(auth["client_id"], auth["client_secret"])
    client_OAuth = make_spotify_client(
        auth["client_id"],
        auth["client_secret"],
        auth["redirect_uri"],
        return_OAuth=True,
    )
    if mode == "tracks":
        track_ids = read_tracks(file_in)
    elif mode == "albums":
        artist_album_tuples = read_albums(file_in)
        print(f"File {file_in} has {len(artist_album_tuples)} albums. ")
        track_ids = albums_to_track_ids(
            artist_album_tuples,
            client,
            min_sim_artist=min_sim_artist,
            min_sim_album=min_sim_album,
        )
    elif mode == "artists":
        artist_names = read_artists(file_in)
        print(f"File {file_in} has {len(artist_names)} artists.")
        track_ids = artists_to_track_ids(artist_names, client, min_sim=min_sim_artist)
    elif mode == "bandcamp_daily":
        artist_album_tuples = scrape_album_names(file_in)
        print(f"File {file_in} has {len(artist_album_tuples)} albums.")
        track_ids = albums_to_track_ids(
            artist_album_tuples,
            client,
            min_sim_artist=60,
            min_sim_album=60,
        )
        name = Path(file_in).stem
    else:
        raise ValueError(f"Unknown type '{mode}'.")

    if mode != "tracks":
        save_tracks(track_ids, file_out)

    print(f"Adding tracks to playlist...")
    if name and track_ids:
        res = create_playlist(name, auth["user_id"], client_OAuth)
        id = res["id"]
    add_to_playlist(track_ids, id, client_OAuth)
    return None


def make_parser():
    NOW = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    parser = argparse.ArgumentParser(
        description="Import tracks to Spotify playlist. Can import from a list of track IDs, a list of albums, or a list of artists. Can import to a new or an existing Spotify playlist."
    )
    parser.add_argument(
        "file_in",
        type=str,
        help="Input file.",
    )
    parser.add_argument(
        "--mode",
        type=str,
        default="albums",
        choices=["albums", "artists", "tracks", "bandcamp_daily"],
        help="Type of file_in. One of: (i) albums: txt of artist - album or csv with artist and album, (ii) artists: txt of artists (iii) tracks: txt of track IDs",
    )
    parser.add_argument(
        "--name",
        type=str,
        help="Name for new Spotify playlist.",
        default=f"New playlist ({NOW})",
    )
    parser.add_argument(
        "--id",
        type=str,
        help="ID for existing Spotify playlist. Ignored, if name is given.",
    )
    return parser


if __name__ == "__main__":
    import secret

    parser = make_parser()
    args = parser.parse_args()
    auth = {
        "client_id": secret.client_id,
        "client_secret": secret.client_secret,
        "redirect_uri": secret.redirect_uri,
        "user_id": secret.user_id,
    }
    import_to_playlist(
        file_in=args.file_in,
        mode=args.mode,
        name=args.name,
        id=args.id,
        auth=auth,
        file_out=None,
        min_sim_artist=60,
        min_sim_album=60,
    )
