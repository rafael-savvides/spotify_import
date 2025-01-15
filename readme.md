# Spotify import

Import artists, albums, or a bandcamp list page into a Spotify playlist.

```
spotify_import [file] --mode [tracks,artists,albums,bandcamp_daily]
```

`mode` defines what `file` is: 

- tracks: newline-separated list of Spotify track IDs
- artists: newline-separated list of artist names
- albums: newline-separated list of "album - artist"
- bandcamp: an HTML file of a Bandcamp Daily page (they don't allow scraping anymore)
