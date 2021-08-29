import datetime
import pytest
from pylast import md5
from lastdisco import lastfm
from lastdisco.parsers import DiscogsAlbumParser
from .fixtures import AlbumFixtures

fixtures = AlbumFixtures()


def test_builds_client_with_environment_variables(mock_pylast):
    lastfm.build_client()
    mock_pylast.assert_called_with(
        api_key='api_key',
        api_secret='api_secret',
        username='username',
        password_hash=md5('password'),
        )


def test_raises_error_if_variables_missing():
    lastfm.os.environ.pop('LASTFM_USERNAME')
    with pytest.raises(ValueError):
        lastfm.build_client()


def test_scrobbles_tracks(mock_pylast):
    client = lastfm.build_client()
    tracks = [
        {'artist': 'Hurry', 'title': 'Love is Elusive', 'album': 'Guided Meditation', 'duration': 388},
        {'artist': 'Hurry', 'title': 'Shake It Off', 'album': 'Guided Meditation', 'duration': 218},
        ]
    lastfm.scrobble_tracks(client, tracks)
    timestamp = datetime.datetime(2021, 8, 28, 0, 6, 28).timestamp()
    client.scrobble.assert_called_with(
        artist='Hurry',
        title='Shake It Off',
        timestamp=timestamp,
        album='Guided Meditation',
        duration=218,
        )


def test_ignores_duration_if_below_lastfm_threshold(mock_pylast):
    client = lastfm.build_client()
    tracks = [
        {'artist': 'Tony Molina', 'title': 'Sick Ass Riff', 'album': 'Dissed and Dismissed', 'duration': 25},
        ]
    lastfm.scrobble_tracks(client, tracks)
    assert client.scrobble.call_args[1]['duration'] is None


def test_defaults_to_three_minute_song_length_for_scrobble_offset(mock_pylast):
    tracks = DiscogsAlbumParser(fixtures['umbrellas'])
    client = lastfm.build_client()
    timestamp = datetime.datetime(2021, 8, 28, 0, 33).timestamp()
    lastfm.scrobble_tracks(client, tracks)
    assert client.scrobble.call_args[1]['timestamp'] == timestamp


def test_uses_given_starting_point(mock_pylast):
    tracks = DiscogsAlbumParser(fixtures['france_gall'])
    client = lastfm.build_client()
    start = datetime.datetime(2021, 8, 29, 0, 0)
    lastfm.scrobble_tracks(client, tracks, start=start)
    expected = datetime.datetime(2021, 8, 29, 0, 26, 24).timestamp()
    assert client.scrobble.call_args[1]['timestamp'] == expected


def test_calculates_from_endpoint(mock_pylast):
    tracks = DiscogsAlbumParser(fixtures['france_gall'])
    client = lastfm.build_client()
    end = datetime.datetime(2021, 8, 28, 0, 0)
    lastfm.scrobble_tracks(client, tracks, end=end)
    expected = datetime.datetime(2021, 8, 27, 23, 57, 25).timestamp()
    assert client.scrobble.call_args[1]['timestamp'] == expected
