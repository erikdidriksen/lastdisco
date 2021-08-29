from lastdisco import retrieval


def test_gets_and_parses_page(html):
    assert retrieval.retrieve_album('url')[0]['artist'] == 'France Gall'
