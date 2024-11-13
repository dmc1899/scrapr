"""
Parse HTML content.
"""

from typing import Any

from autoscraper import AutoScraper


class Parser:
    def __init__(self, url: str, wanted_list: list[str]):
        self.parser = _create_custom_parser(url, wanted_list)

    def get_result(self, url: str) -> Any:
        return self.parser.get_result_similar(url)

    def get_results(self, urls: list[str]) -> list[list[str]]:
        return [self.get_result(url) for url in urls]


def _create_custom_parser(url: str, wanted_list: list[str]) -> AutoScraper:
    parser = AutoScraper()
    _ = parser.build(url, wanted_list)
    return parser
