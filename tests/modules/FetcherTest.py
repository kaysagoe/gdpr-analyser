import unittest
from unittest.mock import Mock, patch

from api.models.ApiException import ApiException
from api.modules.Fetcher import Fetcher


class FetcherTest(unittest.TestCase):
    def setUp(self) -> None:
        self.driver = Mock()

    @patch('api.modules.Fetcher.requests')
    def test_should_return_source_with_valid_url(self, mock_requests):
        self.driver.page_source = "Hello World"
        response_mock = Mock()
        response_mock.status_code = 200
        mock_requests.get.return_value = response_mock

        self.assertEqual("Hello World", Fetcher.fetch("http://www.example.com/page", self.driver))

    def test_should_raise_exception_on_empty_url(self):
        with self.assertRaises(ApiException):
            Fetcher.fetch("", self.driver)

    def test_should_raise_exception_on_informal_url(self):
        with self.assertRaises(ApiException):
            Fetcher.fetch("www.example.com", self.driver)

    def test_should_raise_exception_on_invalid_url(self):
        with self.assertRaises(ApiException):
            Fetcher.fetch("example", self.driver)

    @patch("api.modules.Fetcher.requests")
    def test_should_raise_exception_when_source_is_empty(self, mock_requests):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_requests.get.return_value = mock_response
        self.driver.page_source = ""
        with self.assertRaises(ApiException):
            Fetcher.fetch("http://www.example.com/page", self.driver)

    @patch("api.modules.Fetcher.requests")
    def test_should_raise_exception_on_404_response_code(self, mock_requests):
        response_mock = Mock()
        response_mock.status_code = 404
        mock_requests.get.return_value = response_mock

        with self.assertRaises(ApiException):
            Fetcher.fetch("http://www.example.com/page", self.driver)


if __name__ == '__main__':
    unittest.main()
