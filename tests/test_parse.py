import pytest
from unittest.mock import Mock, patch
from scrapr.action.parse import Parser, _create_custom_parser

@pytest.fixture
def mock_autoscraper():
    with patch('your_module.AutoScraper') as mock:
        yield mock

def test_parser_initialization(mock_autoscraper):
    url = "https://example.com"
    wanted_list = ["item1", "item2"]
    parser = Parser(url, wanted_list)

    mock_autoscraper.assert_called_once()
    mock_autoscraper().build.assert_called_once_with(url, wanted_list)
    assert parser.parser == mock_autoscraper().build.return_value

def test_get_result(mock_autoscraper):
    url = "https://example.com"
    wanted_list = ["item1", "item2"]
    parser = Parser(url, wanted_list)

    test_url = "https://test.com"
    expected_result = ["result1", "result2"]
    parser.parser.get_result_similar.return_value = expected_result

    result = parser.get_result(test_url)

    parser.parser.get_result_similar.assert_called_once_with(test_url)
    assert result == expected_result

def test_get_results(mock_autoscraper):
    url = "https://example.com"
    wanted_list = ["item1", "item2"]
    parser = Parser(url, wanted_list)

    test_urls = ["https://test1.com", "https://test2.com"]
    expected_results = [["result1"], ["result2"]]
    parser.parser.get_result_similar.side_effect = expected_results

    results = parser.get_results(test_urls)

    assert parser.parser.get_result_similar.call_count == len(test_urls)
    parser.parser.get_result_similar.assert_any_call(test_urls[0])
    parser.parser.get_result_similar.assert_any_call(test_urls[1])
    assert results == expected_results

def test_create_custom_parser(mock_autoscraper):
    url = "https://example.com"
    wanted_list = ["item1", "item2"]

    parser = _create_custom_parser(url, wanted_list)

    mock_autoscraper.assert_called_once()
    mock_autoscraper().build.assert_called_once_with(url, wanted_list)
    assert parser == mock_autoscraper().build.return_value
