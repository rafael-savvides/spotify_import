"""Scrape bandcamp lists for album pages."""

from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


def scrape_album_names(html_file: Path) -> list[tuple[str, str]]:
    """Scrape album names from a Bandcamp list page

    Args:
        html_file: HTML file of Bandcamp page.

    Returns:
        List of artist album tuples.
    """
    with open(html_file, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    return [
        (
            albuminfo.find(class_="mpartist").text,
            albuminfo.find(class_="mptralbum").text,
        )
        for albuminfo in soup.find_all("span", class_="mpalbuminfo")
    ]


def scrape_album_links(html_file: Path, tag: str = "h3") -> list[str]:
    """Find links to bandcamp album pages that are in a given HTML tag.

    Args:
        html_file: HTML file that contains links to bandcamp albums.
        Example with h3 heading: https://daily.bandcamp.com/best-ambient/the-best-ambient-on-bandcamp-april-2023.
        tag: HTML tags in which to search for bandcamp albums.

    Returns:
        List of URLs to bandcamp album pages.
    """
    with open(html_file, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    links = [h.find("a") for h in soup.find_all(tag)]
    return [
        l.get("href")
        for l in links
        if l and l.get("href").find("bandcamp.com/album/") != -1
    ]


def scrape_artist_album(html_file: Path) -> tuple[str, str] | tuple[None, None]:
    """Get artist name and album name from a Bandcamp album page.

    Args:
        html_file: HTML file of album page. Example: https://timhecker.bandcamp.com/album/no-highs.

    Returns
        artist name, album name
    """
    with open(html_file, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    title = soup.find("title").get_text()
    album_artist = title.split(" | ")
    if len(album_artist) > 1:
        return album_artist[1].strip(), album_artist[0].strip()
    return None, None


if __name__ == "__main__":
    import sys

    args = sys.argv
    file = Path(args[1])

    l = scrape_album_names(file)

    filename = f"{file.name}.csv"
    df = pd.DataFrame(l, columns=["artist", "album"])
    df.to_csv(filename, index=False)
    print(f"Saved to {filename}.")
