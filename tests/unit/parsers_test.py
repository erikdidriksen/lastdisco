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


def test_ignores_side_if_unavailable():
    album = fixtures['pete_astor']
    assert DiscogsAlbumParser(album)[0]['side'] is None


def test_ignores_duration_if_unavailable():
    album = fixtures['umbrellas']
    assert DiscogsAlbumParser(album)[0]['duration'] is None


def test_ignores_discogs_disambiguation():
    album = fixtures['umbrellas']
    assert DiscogsAlbumParser(album)[0]['artist'] == 'The Umbrellas'
