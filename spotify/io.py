import csv


def read_tracks(file):
    """Read a text file of Spotify track IDs into a list."""
    with open(file, encoding="utf8") as f:
        track_ids = f.readlines()
    return sanitize(track_ids)


def read_albums(file: str) -> list[tuple[str, str]]:
    """Read file into artist-album tuples

    Args:
        file (str): Filename. One of (i) txt of 'artist - album' lines, (ii) csv with artist and album headers.

    Returns:
        List[Tuple[str, str]]: list of (artist, album) tuples
    """
    if file.endswith(".txt"):
        with open(file, encoding="utf8") as f:
            albums = f.readlines()
        albums = sanitize(albums)
        artist_albums = [tuple(x.split(" - ", 1)) for x in albums]
    elif file.endswith(".csv"):
        header = True
        artist_albums = []
        with open(file, encoding="utf8") as f:
            reader = csv.reader(f, delimiter=",")
            if header:
                next(reader, None)  # skip the header
            for row in reader:
                artist_albums.append((row[0], row[1]))
    else:
        raise ValueError("file should be either .txt or .csv.")
    return artist_albums


def read_artists(file) -> list[str]:
    """Read a text file of artists into a list."""
    with open(file, encoding="utf8") as f:
        artists = f.readlines()
    return sanitize(artists)


def save_tracks(l: list, file: str):
    """Save keys of a list l into line-separated file."""
    with open(file, mode="w") as f:
        f.write("\n".join(l))
    print(f"Saved {len(l)} tracks to {file}.")


def sanitize(l: list[str]):
    """Sanitize list of strings

    Remove empty strings and strings starting with //."""
    return [
        e.replace("\n", "") for e in l if e not in ["", "\n"] and not e.startswith("//")
    ]
