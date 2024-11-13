from typing import Dict, Callable, Any

from scrapr.config import load_config
from scrapr.sites import uic
from scrapr.action.parse import Parser
from scrapr.action.persist import write_to_csv
from scrapr.action.scrape import Scraper
from scrapr.model.command import create_command


def _get_params() -> Dict[str, Any]:
    return {
        'start_url': 'https://ulsterindependentclinic.com/consultants/',
        'query_parameter_key': '?page_2826c=',
        'total_pages': 1,
        'filter_url': 'https://ulsterindependentclinic.com/consultant/',
        'sample_url': 'https://ulsterindependentclinic.com/consultant/3353330/',
        'wanted_list': ["Mr. Robin Adair", "ENT", "3353330", "Adults & Children", "028 9068 7444"],
        'output_file': 'uic_consultant_contacts.csv',
    }


def _get_config() -> Dict[str, str]:
    return load_config()


def _get_writer() -> Callable[[list[dict[str, str]], str], None]:
    return write_to_csv


def _create_parser(url: str, wanted_list: list[str]) -> Parser:
    return Parser(url, wanted_list)


def _create_scraper(api_url: str, api_key: str) -> Scraper:
    return Scraper(api_url, api_key)


def main() -> None:
    app_config: Dict[str, str] = _get_config()
    params: Dict[str, Any] = _get_params()

    parser: Parser = _create_parser(params['sample_url'], params['wanted_list'])
    scraper: Scraper = _create_scraper(api_url=app_config['SCRAPER_API_URL'], api_key=app_config['SCRAPER_API_KEY'])
    writer: Callable[[list[dict[str, str]], str], None] = _get_writer()

    command_input = [
        params['start_url'],
        params['query_parameter_key'],
        params['total_pages'],
        params['filter_url'],
        params['sample_url'],
        params['wanted_list'],
        scraper,
        parser,
        writer,
        params['output_file'],
    ]

    uic.execute(create_command(command_input))


if __name__ == "__main__":
    main()
