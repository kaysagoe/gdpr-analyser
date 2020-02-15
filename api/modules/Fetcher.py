from selenium.webdriver.chrome.webdriver import WebDriver
import requests
import re

from api.models.ApiException import ApiException


class Fetcher:
    @staticmethod
    def fetch(url: str, driver: WebDriver) -> str:
        if re.fullmatch("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+",
                        url.strip()) is None:
            raise ApiException("Invalid Input", "Invalid URL input string", 400)

        response = requests.get(url)
        if response.status_code == 200:
            driver.implicitly_wait(10)
            driver.get(url)
            if driver.page_source == "" or driver.page_source is None:
                raise ApiException("Invalid Input", "URL returned empty source", 400)
            else:
                return driver.page_source
        else:
            raise ApiException("Invalid Input", "URL returned 404 error code", 400)
