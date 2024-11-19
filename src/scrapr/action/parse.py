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

# """
# Parse HTML content.
# """
# from typing import Any, List, Dict, Callable, NamedTuple, TypeVar
# from autoscraper import AutoScraper
# from functools import partial
#
# # Type definitions for clarity
# Url = str
# WantedContent = str
# ParserResult = List[str]
#
# # Use a NamedTuple instead of a dataclass for immutable configuration
# class ParserConfig(NamedTuple):
#     initial_url: Url
#     wanted_list: List[WantedContent]
#
# # Create type alias for our parser function
# ParserFn = Callable[[Url], ParserResult]
#
# def initialize_parser(config: ParserConfig) -> AutoScraper:
#     """
#     Creates and configures an AutoScraper instance
#     Note: This is our only impure function that deals with AutoScraper directly
#     """
#     parser = AutoScraper()
#     parser.build(config.initial_url, config.wanted_list)
#     return parser
#
# def create_parser_fn(auto_scraper: AutoScraper) -> ParserFn:
#     """
#     Creates a pure function that wraps the AutoScraper instance
#     """
#     return lambda url: auto_scraper.get_result_similar(url)
#
# def get_result(parser_fn: ParserFn, url: Url) -> ParserResult:
#     """
#     Pure function to get results for a single URL
#     """
#     return parser_fn(url)
#
# def get_results(parser_fn: ParserFn, urls: List[Url]) -> List[ParserResult]:
#     """
#     Pure function to get results for multiple URLs
#     """
#     return [get_result(parser_fn, url) for url in urls]
#
# # Function composition helper
# def compose(f: Callable, g: Callable) -> Callable:
#     """
#     Compose two functions: f(g(x))
#     """
#     return lambda x: f(g(x))
#
# # Higher-order function to create a configured scraping function
# def create_scraping_fn(config: ParserConfig) -> ParserFn:
#     """
#     Creates a function that can be used for scraping
#     Composes the initialization and parser creation
#     """
#     return compose(create_parser_fn, initialize_parser)(config)
