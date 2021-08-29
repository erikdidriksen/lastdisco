import pytest
from .fixtures import AlbumFixtures
from lastdisco.parsers import DiscogsAlbumParser

fixtures = AlbumFixtures()


def test_parses_all_tracks():
    album = fixtures['france_gall']
    assert len(DiscogsAlbumParser(album)) == 12


@pytest.mark.parametrize('key, expected', [
    ('artist', 'France Gall'),
    ('album', 'Poupée De Cire Poupée De Son'),
    ('title', 'Poupée De Cire, Poupée De Son'),
    ('duration', 150),
    ('side', 'A'),
    ('sequence', 1),
    ])
def test_parses_track_details(key, expected):
    album = fixtures['france_gall']
    assert DiscogsAlbumParser(album)[0][key] == expected
