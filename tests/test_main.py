import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any, Callable

from scrapr.main import (_get_params, _get_config, _get_writer, _create_parser,
                 _create_scraper, main)
from scrapr.action.parse import Parser
from scrapr.action.scrape import Scraper

@pytest.fixture
def mock_config():
    return {
        'SCRAPER_API_URL': 'https://api.example.com',
        'SCRAPER_API_KEY': 'test_key'
    }

@pytest.fixture
def expected_params():
    return {
        'start_url': 'https://ulsterindependentclinic.com/consultants/',
        'query_parameter_key': '?page_2826c=',
        'total_pages': 1,
        'filter_url': 'https://ulsterindependentclinic.com/consultant/',
        'sample_url': 'https://ulsterindependentclinic.com/consultant/3353330/',
        'wanted_list': ["Mr. Robin Adair", "ENT", "3353330", "Adults & Children", "028 9068 7444"],
        'output_file': 'uic_consultant_contacts.csv',
    }

def test_get_writer():
    writer = _get_writer()
    from scrapr.action.persist import write_to_csv

    assert writer == write_to_csv

def test_create_scraper():
    api_url = "https://api.example.com"
    api_key = "test_key"

    scraper = _create_scraper(api_url, api_key)

    assert isinstance(scraper, Scraper)
    assert scraper.api_url == api_url
    assert scraper.api_key == api_key
