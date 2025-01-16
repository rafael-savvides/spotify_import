import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth


def make_spotify_client(
    client_id: str,
    client_secret: str,
    redirect_uri: str = None,
    return_OAuth: bool = False,
) -> tuple[spotipy.Spotify, spotipy.Spotify]:
    """Create Spotify client

    Args:
        client_id (str): Client ID.
        client_secret (str): Client secret.
        redirect_uri (str): Redirect URI.
        return_OAuth (bool): If True, returns OAuth client that can edit user playlists, but has lower rate limit.

    Returns:
        spotipy.Spotify: spotipy.Spotify client.
    """
    if not return_OAuth:
        return spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
                client_id=client_id, client_secret=client_secret
            )
        )
    else:
        # SpotifyOAuth can edit user playlists, but has lower rate limit.
        return spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=client_id,
                client_secret=client_secret,
                redirect_uri=redirect_uri,
                scope="playlist-modify-public playlist-modify-private",
            )
        )


def create_playlist(
    name: str, user_id: str, client_OAuth: SpotifyOAuth, description: str = ""
) -> dict:
    """Create Spotify playlist. Returns dict of playlist properties.
    (id, public, name, type, description, tracks, etc)."""
    return client_OAuth.user_playlist_create(
        user=user_id, name=name, public=False, description=description
    )


def add_to_playlist(
    track_ids: list[str], playlist_id: str, client_OAuth: SpotifyOAuth
) -> None:
    """Add tracks to a Spotify playlist."""
    # Spotify has a maximum of 100 tracks per request
    max_tracks_per_request = 100
    i = 0
    while i < len(track_ids):
        track_ids_to_add = track_ids[i : (i + max_tracks_per_request)]
        client_OAuth.playlist_add_items(playlist_id, track_ids_to_add)
        i = i + max_tracks_per_request
    print(f"Added {len(track_ids)} tracks to playlist {playlist_id}.")
    return None
