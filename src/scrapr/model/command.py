from typing import Dict, List, Any

from scrapr.action.parse import Parser
from scrapr.action.scrape import Scraper


def create_command(params: List[Any]) -> Dict[str, Any]:
    if len(params) != 10:
        raise ValueError("Expected 10 parameters")

    keys = [
        'start_url',
        'query_parameter_key',
        'total_pages',
        'filter_url',
        'sample_url',
        'wanted_list',
        'scraper',
        'parser',
        'writer',
        'output_file',
    ]

    command = dict(zip(keys, params))

    if not isinstance(command['start_url'], str):
        raise TypeError("start_url must be a string")
    if not isinstance(command['query_parameter_key'], str):
        raise TypeError("query_parameter_key must be a string")
    if not isinstance(command['total_pages'], int):
        raise TypeError("total_pages must be an integer")
    if not isinstance(command['filter_url'], str):
        raise TypeError("filter_url must be a string")
    if not isinstance(command['sample_url'], str):
        raise TypeError("sample_url must be a string")
    if not isinstance(command['wanted_list'], list):
        raise TypeError("wanted_list must be a list")
    if not isinstance(command['scraper'], Scraper):
        raise TypeError("scraper must be an instance of Scraper")
    if not isinstance(command['parser'], Parser):
        raise TypeError("parser must be an instance of Parser")
    if not callable(command.get('writer')):
        raise TypeError("writer must be a callable function")
    if not isinstance(command['output_file'], str):
        raise TypeError("output_file must be a string")
    return command
