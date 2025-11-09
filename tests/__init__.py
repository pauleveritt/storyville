"""Test suite for the storytime package."""

from typing import TypedDict, Dict
from xml.etree import ElementTree

import requests

x = requests.get("https://www.p ython.org")
dom = ElementTree.fromstring("<x>foo</x>")


class Episode(TypedDict):
    id: int


episodes: dict[str, Episode] = {}


def foo():
    x = episodes.get("x")
    return z


class Foo:

    @classmethod
    def load(cls):
        return 9
