import os
from bs4 import BeautifulSoup as Soup


class AlbumFixtures:
    """A dict-like interface for loading fixtures."""

    def __init__(self):
        self._fixtures = dict()
        self.folder = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            os.pardir,
            'fixtures',
            )

    def __getitem__(self, key):
        if key not in self._fixtures:
            self._fixtures[key] = self._load_fixture(key)
        return self._fixtures[key]

    def _load_fixture(self, key):
        """Load the given fixture."""
        path = os.path.join(self.folder, f'{key}.html')
        print(path)
        with open(path) as fixture_file:
            return Soup(fixture_file.read(), 'html.parser')
