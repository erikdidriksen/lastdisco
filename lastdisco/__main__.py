import sys
from .cli import parse_args
from .lastfm import build_client, scrobble_tracks
from .retrieval import retrieve_album


def run_module(url, username=None, password=False, end=False, side=None):
    """Scrobble the album from the given URL."""
    client = build_client(username=username, password=password)
    tracks = retrieve_album(url)
    end = True if end else False
    scrobble_tracks(client, tracks, end=end, side=side)
    album = tracks[0]['album']
    print(f'Scrobbled "{album}" for user {client.username}.')


if __name__ == '__main__':
    params = parse_args(sys.argv[1:])
    run_module(**params)
