"""Contains various utility functions."""

import time
import cProfile, pstats, io
from urllib import parse
from functools import wraps
from bs4 import BeautifulSoup

from cambridge.settings import DICTS


def make_a_soup(text):
    soup = BeautifulSoup(text, "lxml")
    return soup


def replace_all(string):
    return (
        string.replace("\n            (", "(")
        .replace("(\n    \t                ", "(")
        .replace("\n", " ")
        .replace("      \t                ", " ")
        .replace("\\'", "'")
        .replace("  ", " ")
        .replace("\xa0 ", "")
        .replace("[ ", "[")
        .replace(" ]", "]")
        .replace("A1", "")
        .replace("A2", "")
        .replace("B1", "")
        .replace("B2", "")
        .replace("C1", "")
        .replace("C2", "")
        .strip()
    )


def parse_response_url(url, dict):
    """Return the unquoted url for displaying and saving."""

    url = parse.unquote(url)

    if dict == DICTS[0]:
        response_base_url = url.split("?")[0]
        return response_base_url

    return url 


def construct_request_url(url, input_word, dict):
    """Return the url formatted for requesting the web page at the url."""
    
    if dict == DICTS[0]:
        query_word = input_word.replace(" ", "-").replace("/", "-")
        request_url = url + query_word
        return request_url
    
    return url + parse.quote(input_word)


def construct_request_url_spellcheck(url, input_word):
    """Return the url formatted for requesting the spellcheck web page at the url."""

    query_word = input_word.replace(" ", "+").replace("/", "+")
    request_url = url + query_word

    return request_url


def profile(func):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner


def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_at = time.time()
        f = func(*args, **kwargs)
        time_taken = round((time.time() - start_at), 2)
        print("\nTime taken: {} seconds".format(time_taken))
        return f

    return wrapper
