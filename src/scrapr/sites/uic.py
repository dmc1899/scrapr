from functools import partial
from typing import List, Dict, Any, Callable

from scrapr.action.parse import Parser
from scrapr.action.scrape import Scraper
from scrapr.model import contact


def execute(command: Dict[str, Any]) -> None:
    scraper: Scraper = command.get('scraper')  # type: ignore
    parser: Parser = command.get('parser')  # type: ignore
    write: Callable[List[Dict[str, str]], None] = command.get('writer')  # type: ignore
    filter_url: str = command.get('filter_url')  # type: ignore
    start_url: str = command.get('start_url')  # type: ignore
    query_parameter_key: str = command.get('query_parameter_key')  # type: ignore
    total_pages: int = command.get('total_pages')  # type: ignore
    output_file: str = command.get('output_file')  # type: ignore

    get_contact_urls = partial(_get_contact_urls, filter_url=filter_url, scraper=scraper)

    target_urls = _get_target_urls(
        start_url=start_url,
        query_parameter_key=query_parameter_key,
        total_pages=total_pages,
        scraper=scraper,
    )

    contact_urls = get_contact_urls(target_urls)
    contacts_list = parser.get_results(contact_urls)

    write(contact.create_contacts_from(contacts_list), output_file)


def _get_contact_urls(target_urls: List[str], filter_url: str, scraper: Scraper) -> List[str]:
    return scraper.extract_urls_from_targets(target_urls=target_urls, filter_url=filter_url)


def _get_target_urls(start_url: str, query_parameter_key: str, total_pages: int, scraper: Scraper) -> List[str]:
    return scraper.get_target_contact_urls(start_url, query_parameter_key, total_pages)
