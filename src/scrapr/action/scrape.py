"""
Scrape web pages from websites.
"""

from typing import Set, List, Optional
from functools import reduce
from collections import deque
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

class ScraperAPICreditsExhaustedException(Exception):
    def __init__(self, message="No credits remaining in Scraper API account"):
        self.message = message
        super().__init__(self.message)


class Scraper:
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key

    def _get_html_using_scraper_api(self, target_url: str, auto_parse: str = 'false') -> str:
        try:
            payload = {'api_key': self.api_key, 'url': target_url, 'render': 'true', 'autoparse': auto_parse}
            response = requests.get(url=self.api_url, params=payload, timeout=30)
            response.raise_for_status()
            return response.text
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                error_body = e.response.content if e.response.content else {}
                if "credits" in str(error_body).lower() or "quota" in str(error_body).lower():
                    raise ScraperAPICreditsExhaustedException(
                        f"Scraper API credits exhausted: {error_body}"
                    )
                raise RequestException(f"Access forbidden (403). Please check your API key and permissions: {str(e)}")
            raise RequestException(f"HTTP error occurred: {str(e)}")
        except requests.RequestException as e:
            raise e

    @staticmethod
    def _is_valid_url(url: str, url_part: str, path_part: Optional[str] = None) -> bool:
        return url.startswith(url_part) and (path_part is None or path_part in url)

    def get_html_from(self, target_url: str) -> str:
        return self._get_html_using_scraper_api(target_url=target_url)

    @staticmethod
    def get_target_contact_urls(base_url: str, query_parameter_key: str, total_pages: int) -> list[str]:
        def _get_page_range(end: int) -> range:
            return range(1, end + 1)

        return [
            f"{base_url}{query_parameter_key}{query_parameter_value}"
            for query_parameter_value in _get_page_range(total_pages)
        ]

    def extract_urls_from_targets(self, target_urls: list[str], filter_url: str) -> List[str]:
        def _flatten(list_of_sets: list[set]) -> list:
            combined_set = reduce(lambda x, y: x | y, list_of_sets)
            return list(combined_set)

        return _flatten([self._extract_urls_from_target(target_url, filter_url) for target_url in target_urls])

    def _extract_urls_from_target(self, target_url: str, filter_url: str) -> Set[str]:
        base_url = target_url.rstrip('/')
        print(f'base_url is {base_url}')

        visited = set()
        to_visit = deque([base_url])

        while to_visit:
            current_url = to_visit.popleft()
            if current_url in visited:
                continue

            print(f"Crawling: {current_url}")
            visited.add(current_url)

            try:
                response = self.get_html_from(current_url)
                soup = BeautifulSoup(response, 'html.parser')

                new_urls = {
                    urljoin(base_url, link['href'])
                    for link in soup.find_all('a', href=True)
                    if self._is_valid_url(urljoin(base_url, link['href']), filter_url)
                }

                to_visit.extend(new_urls - visited)

            except (RequestException, OSError) as e:
                print(f"An error occurred: {e}. Continuing...")

        return visited
