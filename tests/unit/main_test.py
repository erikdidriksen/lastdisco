import datetime
import pytest
from lastdisco import __main__ as main


@pytest.fixture(autouse=True)
def mock_print(mocker):
    return mocker.patch('builtins.print')


def test_creates_playlists(mock_pylast):
    main.run_module(url='url')
    client = mock_pylast.return_value
    client.scrobble.assert_called_with(
        artist='France Gall',
        title='Bonne Nuit',
        timestamp=datetime.datetime(2021, 8, 28, 0, 26, 24).timestamp(),
        album='Poupée De Cire Poupée De Son',
        duration=155,
       )


def test_respects_end_flag(mock_pylast):
    main.run_module(url='url', end=True)
    client = mock_pylast.return_value
    client.scrobble.assert_called_with(
        artist='France Gall',
        title='Bonne Nuit',
        timestamp=datetime.datetime(2021, 8, 27, 23, 57, 25).timestamp(),
        album='Poupée De Cire Poupée De Son',
        duration=155,
        )
