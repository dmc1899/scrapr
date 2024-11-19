import pytest
from unittest.mock import Mock, patch
from typing import Dict, Any

# Assuming the module is named 'site_processor'
from scrapr.sites.uic import execute, _get_contact_urls, _get_target_urls

@pytest.fixture
def mock_scraper():
    scraper = Mock()
    scraper.extract_urls_from_targets.return_value = [
        "https://example.com/contact1",
        "https://example.com/contact2"
    ]
    scraper.get_target_contact_urls.return_value = [
        "https://example.com/page1",
        "https://example.com/page2"
    ]
    return scraper

@pytest.fixture
def mock_parser():
    parser = Mock()
    parser.get_results.return_value = [
        {"name": "Contact 1", "email": "contact1@example.com"},
        {"name": "Contact 2", "email": "contact2@example.com"}
    ]
    return parser

@pytest.fixture
def mock_writer():
    return Mock()

@pytest.fixture
def command_dict(mock_scraper, mock_parser, mock_writer):
    return {
        "scraper": mock_scraper,
        "parser": mock_parser,
        "writer": mock_writer,
        "filter_url": "https://example.com",
        "start_url": "https://example.com/start",
        "query_parameter_key": "?page=",
        "total_pages": 2,
        "output_file": "output.csv"
    }

def test_get_target_urls(mock_scraper):
    start_url = "https://example.com"
    query_parameter_key = "?page="
    total_pages = 2

    result = _get_target_urls(
        start_url=start_url,
        query_parameter_key=query_parameter_key,
        total_pages=total_pages,
        scraper=mock_scraper
    )

    mock_scraper.get_target_contact_urls.assert_called_once_with(
        start_url,
        query_parameter_key,
        total_pages
    )
    assert result == mock_scraper.get_target_contact_urls.return_value

def test_get_contact_urls(mock_scraper):
    target_urls = ["https://example.com/page1", "https://example.com/page2"]
    filter_url = "https://example.com"

    result = _get_contact_urls(
        target_urls=target_urls,
        filter_url=filter_url,
        scraper=mock_scraper
    )

    mock_scraper.extract_urls_from_targets.assert_called_once_with(
        target_urls=target_urls,
        filter_url=filter_url
    )
    assert result == mock_scraper.extract_urls_from_targets.return_value

def test_execute_full_flow(command_dict):
    # Execute the main function
    execute(command_dict)

    # Verify scraper calls
    command_dict["scraper"].get_target_contact_urls.assert_called_once_with(
        command_dict["start_url"],
        command_dict["query_parameter_key"],
        command_dict["total_pages"]
    )

    target_urls = command_dict["scraper"].get_target_contact_urls.return_value
    command_dict["scraper"].extract_urls_from_targets.assert_called_once_with(
        target_urls=target_urls,
        filter_url=command_dict["filter_url"]
    )

    # Verify parser calls
    contact_urls = command_dict["scraper"].extract_urls_from_targets.return_value
    command_dict["parser"].get_results.assert_called_once_with(contact_urls)

    # Verify writer calls
    contacts_list = command_dict["parser"].get_results.return_value
    command_dict["writer"].assert_called_once()

def test_execute_with_missing_parameters():
    incomplete_command = {}
    with pytest.raises(AttributeError):
        execute(incomplete_command)

@patch('scrapr.model.contact.create_contacts_from')
def test_execute_with_contact_creation(mock_create_contacts, command_dict):
    mock_create_contacts.return_value = [
        {"name": "Processed Contact 1", "email": "processed1@example.com"},
        {"name": "Processed Contact 2", "email": "processed2@example.com"}
    ]

    execute(command_dict)

    # Verify contact creation was called
    mock_create_contacts.assert_called_once_with(
        command_dict["parser"].get_results.return_value
    )

    # Verify writer was called with processed contacts
    command_dict["writer"].assert_called_once_with(
        mock_create_contacts.return_value,
        command_dict["output_file"]
    )

def test_execute_with_empty_results(command_dict):
    # Modify mock to return empty results
    command_dict["scraper"].extract_urls_from_targets.return_value = []
    command_dict["parser"].get_results.return_value = []

    execute(command_dict)

    # Verify the flow still completes
    command_dict["parser"].get_results.assert_called_once_with([])
    command_dict["writer"].assert_called_once()

def test_execute_validates_required_parameters():
    required_params = [
        'scraper', 'parser', 'writer', 'filter_url', 'start_url',
        'query_parameter_key', 'total_pages', 'output_file'
    ]

    for param in required_params:
        command = {k: Mock() for k in required_params}
        del command[param]

        with pytest.raises(AttributeError):
            execute(command)
