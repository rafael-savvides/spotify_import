from collections import namedtuple

import spotipy
from thefuzz import fuzz  # String similarity.

NameID = namedtuple("NameID", "name id")
# TODO Use Artist, Album, Track.


def find_artist(
    name: str, client: spotipy.Spotify, min_sim: float = 0
) -> NameID | None:
    """Search for an artist on Spotify using their name.

    - When `name` matches multiple Spotify artists, returns the most similar.
    - When `name` matches no Spotify artist with at least min_sim similarity, returns None.

    Args:
        name: Artist name.
        client: Spotify client.
        min_sim: Minimum similarity of result to the queried name.

    Returns:
        Artist name and their Spotify ID.
    """
    # https://developer.spotify.com/documentation/web-api/reference/#/operations/search
    res = client.search(name, type=["artist"])
    artists = [NameID(id=a["id"], name=a["name"]) for a in res["artists"]["items"]]
    if len(artists) == 0:
        return None
    sims = [string_sim(a.name, name) for a in artists]
    i_max_sim, max_sim = max(enumerate(sims), key=lambda x: x[1])
    if max_sim < min_sim:
        return None
    else:
        return artists[i_max_sim]


def find_album(
    artist_name: str,
    album_name: str,
    client: spotipy.Spotify,
    min_sim_artist: float = 0,
    min_sim_album: float = 0,
) -> NameID | None:
    """Search for an album on Spotify using the artist name and the album name.

    - When `artist_name` or `album_name` match multiple Spotify artists or albums, returns the most similar.
    - When there are no matches with at least `min_sim_artist` similarity to `artist_name`
    and `min_sim_album` similarity to `album_name`, returns None.

    Args:
        artist_name: Artist name.
        album_name: Album name.
        client: Spotify API client.
        min_sim_artist: Minimum similarity of result to queried name. Defaults to 0.
        min_sim_album: Minimum similarity of result to queried name. Defaults to 0.

    Returns:
        Album name and its Spotify ID.
    """
    artist = find_artist(artist_name, client, min_sim=min_sim_artist)
    if not artist:
        return None
    artist_albums = get_artist_albums(artist.id, client)
    if len(artist_albums) == 0:
        return None
    sims = [string_sim(a.name, album_name) for a in artist_albums]
    i_max, max_sim = max(enumerate(sims), key=lambda x: x[1])
    if max_sim < min_sim_album:
        return None
    else:
        return artist_albums[i_max]


def albums_to_track_ids(
    artist_album_tuples: list[tuple[str, str]],
    client: spotipy.Spotify,
    min_sim_artist: float = 0,
    min_sim_album: float = 0,
    verbose: bool = True,
) -> list[str]:
    """Create list of track IDs from a list of artist and album names

    Known issue: Doesn't work with Various Artists.

    Args:
        artist_album_tuples: List of artist-album tuples.
        client: Spotify client from spotipy module.
        verbose: Verbosity. Defaults to True.

    Returns:
        List of track IDs.
    """
    if verbose:
        print("Retrieving artist IDs from Spotify API...")
    albums = list(
        set(
            [
                find_album(
                    artist_name, album_name, client, min_sim_artist, min_sim_album
                )
                for artist_name, album_name in artist_album_tuples
            ]
        )
    )
    if verbose:
        print(f"Parsed {len(albums)} albums. ")
    return [
        track.id
        for album in albums
        if album
        for track in get_album_tracks(album.id, client)
    ]


def artists_to_track_ids(
    artist_names: list[str], client: spotipy.Spotify, min_sim: float = 0, verbose=True
) -> list[str]:
    """Create list of track IDs of top tracks from a list of artist names

    Args:
        artist_names: List of artist names.
        client: Spotify client from spotipy module.
        verbose: Verbose. Defaults to True.

    Returns:
        List of track IDs.
    """
    artists = list(set([find_artist(name, client, min_sim) for name in artist_names]))
    if verbose:
        print(f"Found {len(artists)} artist IDs.")
    return [
        track.id
        for artist in artists
        if artist
        for track in get_artist_top_tracks(artist.id, client)
    ]


def get_artist_albums(artist_id: str, client: spotipy.Spotify) -> list[NameID]:
    """Get albums of artist from the artist_id.
    Returns a list of albums of the artist."""
    return [
        NameID(id=x["id"], name=x["name"])
        for x in client.artist_albums(artist_id)["items"]
    ]


def get_album_tracks(album_id: str, client: spotipy.Spotify) -> list[NameID]:
    """Get list of album tracks from an album ID."""
    tracks = client.album_tracks(album_id)
    return [NameID(id=track["id"], name=track["name"]) for track in tracks["items"]]


def get_artist_top_tracks(artist_id: str, client: spotipy.Spotify) -> list[NameID]:
    """Get the track IDs of the 10 top tracks of an artist."""
    top_tracks = client.artist_top_tracks(artist_id)["tracks"]
    return [NameID(id=track["id"], name=track["name"]) for track in top_tracks]


def string_sim(s1: str, s2: str) -> float:
    """String similarity based on the Levenshtein (edit) distance

    Args:
        s1,s2: Strings.

    Returns:
        A score between 0 and 100 based on the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other.
    """
    return fuzz.ratio(s1.lower(), s2.lower())
