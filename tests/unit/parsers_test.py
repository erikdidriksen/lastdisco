import os
import pytest
from lastdisco.parsers import DiscogsAlbumParser


fixture_folder = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    os.pardir,
    'fixtures',
    )
fixture_path = os.path.join(fixture_folder, 'france_gall.html')
with open(fixture_path) as fixture_file:
    album = fixture_file.read()


def test_parses_all_tracks():
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
    assert DiscogsAlbumParser(album)[0][key] == expected
