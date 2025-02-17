import pytest
from playwright.sync_api import sync_playwright

from base.base import BasePage


@pytest.fixture(scope="session")
def page_object():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        base_page = BasePage(browser)
        base_page.configure_storage()
        yield base_page
        browser.close()