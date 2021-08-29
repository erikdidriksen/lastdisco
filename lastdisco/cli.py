import argparse


def parse_args(args):
    """Parse the CLI arguments for the script."""
    parser = argparse.ArgumentParser(
        description='Scrobbles to Last.fm from Discogs album pages',
        add_help=True,
        )
    parser.add_argument(
        'url',
        action='store',
        help='The URL of the Discogs page to scrobble',
        )
    parser.add_argument(
        '-u', '--user',
        action='store',
        default=None,
        required=False,
        help='Your Last.fm username',
        dest='username',
        )
    parser.add_argument(
        '-p', '--password',
        action='store',
        default=None,
        required=False,
        help='Your Last.fm password',
        dest='password',
        )
    return vars(parser.parse_args(args))
