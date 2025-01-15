# Spotify import

Create a Spotify playlist from a list of artists, albums, or a Bandcamp Daily page.

```
spotify_import [file] --mode [tracks,artists,albums,bandcamp_daily]
```

`mode` defines what `file` is: 

- tracks: newline-separated list of Spotify track IDs
- artists: newline-separated list of artist names
- albums: newline-separated list of album names, given as "album - artist"
- bandcamp: an HTML file of a Bandcamp Daily page (this used to be a URL but they don't allow scraping anymore)
