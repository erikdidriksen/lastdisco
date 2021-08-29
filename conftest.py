import datetime
import os
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


@pytest.fixture(scope='session')
def html():
    fixture_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'tests', 'fixtures', 'france_gall.html'
        )
    with open(fixture_path) as fixture_file:
        return fixture_file.read()


@pytest.fixture(autouse=True)
def mock_requests(mocker, html):
    patch = mocker.patch('lastdisco.retrieval.requests')
    patch.get.return_value.content = html
    return patch


@pytest.fixture(autouse=True)
def mock_now(mocker):
    patch = mocker.patch('lastdisco.lastfm.now')
    patch.return_value = datetime.datetime(2021, 8, 28, 0, 0)
    return patch
