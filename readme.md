# Spotify import

Create a Spotify playlist from a list of artists, albums, or a Bandcamp Daily page.

```
spotify_import [file] --mode [tracks,albums,artists,bandcamp_daily]
```

`mode` defines what `file` is: 

- `tracks`: Spotify track IDs (separated by newlines).
- `albums`: Album names, given as "album - artist" (separated by newlines).
- `artists`: Artist names (separated by newlines). For each artist, the playlist contains their top 10 tracks.
- `bandcamp_daily`: HTML file of a Bandcamp Daily page (this used to be a URL but Bandcamp doesn't allow scraping anymore).
