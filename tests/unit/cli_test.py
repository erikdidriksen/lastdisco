import pytest
from lastdisco import cli


def test_parses_url():
    assert cli.parse_args(['url'])['url'] == 'url'


def test_requires_url():
    with pytest.raises(SystemExit):
        cli.parse_args([])
