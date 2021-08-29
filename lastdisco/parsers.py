import re
from bs4 import BeautifulSoup as Soup


def ensure_is_soup(html):
    """Ensure the incoming HTML is parsed as a BeautifulSoup object."""
    return html if isinstance(html, Soup) else Soup(html, 'html.parser')


class DiscogsTrackParser:
    """A parser for individual tracks on Discogs album pages."""

    def __new__(cls, soup, album):
        cells = cls.tags_by_class_prefix('td', soup.find_all())
        side, sequence = cls.split_track_position(cells['trackPos'].text)
        return {
            'artist': album['artist'],
            'title': cls.title(cells),
            'album': album['title'],
            'duration': cls.duration(cells),
            'side': side,
            'sequence': sequence,
            }

    @staticmethod
    def tags_by_class_prefix(tag_name, tags):
        """Return a dictionary of tags, using their class prefixes as keys."""
        return {
            tag.attrs['class'][0].split('_')[0]: tag
            for tag in tags
            if tag.name == tag_name
            }

    @classmethod
    def title(cls, cells):
        """Return the track's title."""
        spans = cls.tags_by_class_prefix('span', cells['trackTitle'])
        return spans['trackTitle'].text

    @staticmethod
    def split_track_position(track_position):
        """Return the side and sequence number for the track."""
        try:
            side, sequence = tuple(track_position)
        except ValueError:
            side = None
            sequence = track_position
        return side, int(sequence)

    @staticmethod
    def duration(cells):
        """Convert the duration string to a total second count."""
        if 'duration' not in cells:
            return None
        duration = cells['duration'].text
        minutes, seconds = duration.split(':')
        return (60 * int(minutes)) + int(seconds)


class DiscogsAlbumParser:
    """A parser for Discogs album pages."""

    ARTIST_PATTERN = r'(.*)(\s\(\d+\))$'

    def __new__(cls, html):
        soup = ensure_is_soup(html)
        album = {
            'artist': cls.artist(soup),
            'title': cls.title(soup),
            }
        return cls.tracks(soup, album)

    @classmethod
    def artist(cls, soup):
        """Return the name of the artist for the album."""
        name = soup.find('h1').find('a').text
        match = re.match(cls.ARTIST_PATTERN, name)
        if match:
            name = match.groups()[0]
        return name

    @staticmethod
    def title(soup):
        """Return the name of the album's title."""
        return [string for string in soup.find('h1').strings][-1]

    @staticmethod
    def tracks(soup, album_details):
        """Return a list of tracks for the album."""
        tracklist = soup.find('section', {'id': 'release-tracklist'})
        return [
            DiscogsTrackParser(track, album_details)
            for track in tracklist.find_all('tr')
            ]
