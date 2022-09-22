import pytest

import narrator.text.web_parser as wp


VALID_URLS = [
    "https://www.reddit.com",
    "http://www.reddit.com/hot/",
    "https://www.reddit.com/r/Python/",
    "http://www.this_site.does_not.exist.xRoU8A5qZF.com",
]

INVALID_URLS = [
    "",
    "some text",
    ["not", "a", "string"],
    "www.reddit.com",
    "ht@tps://www.reddit.com/",
    "www.reddit.fake",
]

REACHABLE_URLS = [
    "https://www.reddit.com",
    "https://xkcd.com/1619/",
    "http://xkcd.com/2529/",
    "https://stackexchange.com/about",
]
UNREACHABLE_URLS = INVALID_URLS + [
    "http://www.this_site.does_not.exist.xRoU8A5qZF.com",
]


def test_is_uri_valid():
    for url in VALID_URLS:
        assert wp.is_uri_valid(url)
        url_obj = wp.Url(url)
        assert url_obj.is_valid
    for url in INVALID_URLS:
        assert not wp.is_uri_valid(url)
        url_obj = wp.Url(url)
        assert not url_obj.is_valid


@pytest.mark.slow
def test_is_url_reachable():
    for url in REACHABLE_URLS:
        assert wp.is_url_reachable(url)
        url_obj = wp.Url(url)
        assert url_obj.is_reachable
    for url in UNREACHABLE_URLS:
        assert not wp.is_url_reachable(url)
        url_obj = wp.Url(url)
        assert not url_obj.is_reachable
