import json
import time

from playwright.sync_api import Browser, Page, sync_playwright
from requests import HTTPError


class BasePage:
    def __init__(self, b: Browser):
        self.browser: Browser | None = b
        self.page: Page | None = None
        self.page_url = ""
        self.check_http_status = True
        self.capture_request = True
        self.context = None
        self.capture_target_urls = []
        self.capture_request_list = {}
        self.last_headers = None
        self.host = None
        self.context_storage: str | None = None

    def store_request(self, request):
        url = request.url
        if self.host and (self.host not in url):
            return
        for u in self.capture_target_urls:
            if u in url:
                self.capture_request_list[u] = url.split("?")[1]
                self.last_headers = request.headers
                if request.post_data is not None:
                    self.capture_request_list[u] = json.loads(request.post_data)

    def request_process(self, request):
        self.store_request(request)
        if self.check_http_status:
            self.raise_for_status(request)

    def setup(self):
        self.page.on("request", self.request_process)

    def configure_storage(self):
        if self.context_storage is not None:
             self.context = self.browser.new_context(storage_state=self.context_storage)
        else:
            self.context = self.browser.new_context()
        self.page: Page = self.context.new_page()
        self.setup()

    def raise_for_status(self, request)-> None:
        def on_response(response):
            status_code = response.status
            if 400 <= status_code < 500:
                raise HTTPError(f"Client Error: {status_code} - {response.status_text} for URL: {response.url}")
            elif 500 <= status_code < 600:
                raise HTTPError(f"Server Error: {status_code} - {response.status_text} for URL: {response.url}")

        response = request.response()
        if response:
            on_response(response)

    def set_page_url(self, p):
        self.page_url = p

    def fill(self, css_tag: str, value):
        e = self.page.locator(css_tag)
        e.fill(value)
        return e

    def type(self, css_tag: str, value):
        e = self.page.locator(css_tag)
        e.type(value)
        return e

    def press_enter(self):
        self.page.keyboard.press('Enter')

    def press(self, css_tag, v):
        e = self.page.locator(css_tag)
        e.press(v)
        return e

    def enter(self, css_tag):
        e = self.page.locator(css_tag)
        e.press("Enter")
        return e

    def click(self, css_tag):
        e = self.page.locator(css_tag)
        e.click()
        return e

    def click_text(self, css_tag, index=None):
        e = self.page.get_by_text(css_tag)
        if index is not None:
            e = e.nth(index)
        e.click()
        return e

    def wait_until(self, selector, timeout=10000):
        try:
            element = self.page.wait_for_selector(selector, timeout=timeout)
            return element
        except TimeoutError:
            raise TimeoutError(f"Element with selector '{selector}' did not appear within {timeout} ms")


def _main():
    with sync_playwright() as p:
        browser: Browser = p.chromium.launch(headless=False)
        b = BasePage(browser)
        p = "https://www.baidu.com"
        b.set_page_url(p)
        b.configure_storage()
        b.page.goto(p)
        b.click_text("《哪吒2》总票房突破120亿", 0)


if __name__ == "__main__":
    _main()