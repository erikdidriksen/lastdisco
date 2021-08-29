import datetime
import os
import pylast


def env_default(value, environment_variable):
    """Return the value of the environment variable if no value is provided."""
    return value if value is not None else os.environ.get(environment_variable)


def build_client(username=None, password=None, api_key=None, api_secret=None):
    """Return a Last.fm client."""
    auth = {
        'username': env_default(username, 'LASTFM_USERNAME'),
        'password': env_default(password, 'LASTFM_PASSWORD'),
        'api_key': env_default(api_key, 'LASTFM_API_KEY'),
        'api_secret': env_default(api_secret, 'LASTFM_API_SECRET'),
        }
    missing = [key for key, value in auth.items() if value is None]
    if missing:
        s = 's' if len(missing) != 1 else ''
        raise ValueError(f'Missing auth key{s}: {",".join(missing)}')
    return pylast.LastFMNetwork(
        api_key=auth['api_key'],
        api_secret=auth['api_secret'],
        username=auth['username'],
        password_hash=pylast.md5(auth['password']),
        )


def now():
    """Return the current datetime."""
    return datetime.datetime.now()  # pragma: no cover


def reported_duration(duration):
    """Return the duration to report to Last.fm."""
    return None if duration is None or duration < 30 else duration


def offset(duration):
    """Return the offset to separate scrobbles."""
    return 180 if duration is None else duration


def start_datetime(dt=None, is_end=False, tracks=None):
    """Return the initial start datetime for the batch of scrobbles."""
    dt = now() if dt is None else dt
    if not is_end:
        return dt
    total_offset = sum(offset(track['duration']) for track in tracks)
    return dt - datetime.timedelta(seconds=total_offset)


def scrobble_tracks(client, tracks, dt=None, is_end=False, side=None):
    """Scrobble the given tracks."""
    dt = start_datetime(dt, is_end, tracks)
    if side is not None:
        tracks = [track for track in tracks if track['side'] == side]
    for track in tracks:
        client.scrobble(
            artist=track['artist'],
            title=track['title'],
            timestamp=dt.timestamp(),
            album=track['album'],
            duration=reported_duration(track['duration']),
            )
        dt += datetime.timedelta(seconds=offset(track['duration']))
