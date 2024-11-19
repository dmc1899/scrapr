import pytest
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from scrapr.action.scrape import Scraper, ScraperServiceCreditsExhaustedException

@pytest.fixture
def scraper():
    return Scraper(api_url="https://api.example.com", api_key="test_key")

@pytest.fixture
def mock_response():
    mock = Mock()
    mock.text = """
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
            <a href="https://other-domain.com/page3">Page 3</a>
        </body>
    </html>
    """
    return mock

def test_scraper_initialization():
    api_url = "https://api.example.com"
    api_key = "test_key"
    scraper = Scraper(api_url=api_url, api_key=api_key)

    assert scraper.api_url == api_url
    assert scraper.api_key == api_key

def test_is_valid_url():
    assert Scraper._is_valid_url("https://example.com/test", "https://example.com")
    assert Scraper._is_valid_url("https://example.com/test", "https://example.com", "test")
    assert not Scraper._is_valid_url("https://other.com/test", "https://example.com")
    assert not Scraper._is_valid_url("https://example.com/other", "https://example.com", "test")

def test_get_target_contact_urls():
    base_url = "https://example.com"
    query_param = "?page="
    total_pages = 3

    expected = [
        "https://example.com?page=1",
        "https://example.com?page=2",
        "https://example.com?page=3"
    ]

    result = Scraper.get_target_contact_urls(base_url, query_param, total_pages)
    assert result == expected

@patch('requests.get')
def test_get_html_using_scraper_api_success(mock_get, scraper, mock_response):
    mock_get.return_value = mock_response
    mock_response.raise_for_status = Mock()

    result = scraper._get_html_using_scraper_api("https://example.com")

    assert result == mock_response.text
    mock_get.assert_called_once()

@patch('requests.get')
def test_get_html_using_scraper_api_credits_exhausted(mock_get, scraper):
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.content = b"No credits remaining"
    mock_get.side_effect = requests.HTTPError(response=mock_response)

    with pytest.raises(ScraperServiceCreditsExhaustedException):
        scraper._get_html_using_scraper_api("https://example.com")

@patch('requests.get')
def test_get_html_using_scraper_api_forbidden(mock_get, scraper):
    mock_response = Mock()
    mock_response.status_code = 403
    mock_response.content = b"Access denied"
    mock_get.side_effect = requests.HTTPError(response=mock_response)

    with pytest.raises(RequestException) as exc_info:
        scraper._get_html_using_scraper_api("https://example.com")
    assert "Access forbidden (403)" in str(exc_info.value)

@patch.object(Scraper, '_get_html_using_scraper_api')
def test_extract_urls_from_target(mock_get_html, scraper):
    html_content = """
    <html>
        <body>
            <a href="/page1">Page 1</a>
            <a href="https://example.com/page2">Page 2</a>
        </body>
    </html>
    """
    mock_get_html.return_value = html_content

    target_url = "https://example.com"
    filter_url = "https://example.com"

    result = scraper._extract_urls_from_target(target_url, filter_url)

    expected_urls = {
        "https://example.com",
        "https://example.com/page1",
        "https://example.com/page2"
    }

    assert result == expected_urls

def test_extract_urls_from_targets(scraper):
    with patch.object(Scraper, '_extract_urls_from_target') as mock_extract:
        mock_extract.side_effect = [
            {"https://example.com/page1"},
            {"https://example.com/page2"}
        ]

        target_urls = ["https://example.com/1", "https://example.com/2"]
        filter_url = "https://example.com"

        result = scraper.extract_urls_from_targets(target_urls, filter_url)

        assert sorted(result) == sorted(["https://example.com/page1", "https://example.com/page2"])
        assert mock_extract.call_count == 2

@patch('requests.get')
def test_get_html_using_scraper_api_timeout(mock_get, scraper):
    mock_get.side_effect = requests.Timeout()

    with pytest.raises(RequestException):
        scraper._get_html_using_scraper_api("https://example.com")

def test_scraper_service_credits_exhausted_exception():
    custom_message = "Custom error message"
    exception = ScraperServiceCreditsExhaustedException(custom_message)
    assert str(exception) == custom_message

    default_exception = ScraperServiceCreditsExhaustedException()
    assert str(default_exception) == "No credits remaining in account."
