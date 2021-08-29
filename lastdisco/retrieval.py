import requests
from .parsers import DiscogsAlbumParser


def retrieve_album_html(url):
    """Return the HTML for the given URL."""
    return requests.get(url).content


def retrieve_album(url):
    """Return the parsed data for the given URL."""
    html = retrieve_album_html(url)
    return DiscogsAlbumParser(html)
