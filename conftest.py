import datetime
import pytest


@pytest.fixture(autouse=True)
def mock_os(mocker):
    mocked = {
        'LASTFM_USERNAME': 'username',
        'LASTFM_PASSWORD': 'password',
        'LASTFM_API_KEY': 'api_key',
        'LASTFM_API_SECRET': 'api_secret',
        }
    return mocker.patch.dict('lastdisco.lastfm.os.environ', mocked)


@pytest.fixture(autouse=True)
def mock_pylast(mocker):
    return mocker.patch('lastdisco.lastfm.pylast.LastFMNetwork')


@pytest.fixture(autouse=True)
def mock_now(mocker):
    patch = mocker.patch('lastdisco.lastfm.now')
    patch.return_value = datetime.datetime(2021, 8, 28, 0, 0)
    return patch
