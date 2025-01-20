# Spotify import

Create a Spotify playlist from a list of artists, albums, or a Bandcamp Daily page.

## Installation

```sh
pip install .
```

## Usage

```sh
spotify-import [file] --mode [tracks,albums,artists,bandcamp_daily]
```

`mode` defines what `file` is: 

- `tracks`: Spotify track IDs (separated by newlines).
- `albums`: Album names, given as "album - artist" (separated by newlines).
- `artists`: Artist names (separated by newlines). For each artist, the playlist contains their top 10 tracks.
- `bandcamp_daily`: HTML file of a Bandcamp Daily page (this used to be a URL but Bandcamp doesn't allow scraping anymore).

## Authentication

See [spotipy](https://github.com/spotipy-dev/spotipy) on authenticating with Spotify's Web API, then set the following environment variables: 

```sh
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'

# Spotify profile in which to create the playlist.
export SPOTIPY_USER_ID='your-spotify-user-id' 
```
