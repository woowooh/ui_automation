from playwright.sync_api import sync_playwright, Browser, Page, Playwright
from requests import HTTPError


class Base:
    def __init__(self):
        self.playwright: Playwright | None = None
        self.browser: Browser | None = None
        self.page: Page | None = None
        self.page_url = ""
        self.check_http_status = False
        self.setup()
        self.cache = {

        }

    def setup(self):
        if self.check_http_status:
            self.page.on("request", self.raise_for_status)

    def configure(self, p):
        self.playwright: Playwright = p
        self.browser: Browser = self.playwright.chromium.launch(headless=False)
        self.page: Page = self.browser.new_page()

    def raise_for_status(self, request)-> None:
        def on_response(response):
            status_code = response.status
            if 400 <= status_code < 500:
                raise HTTPError(f"Client Error: {status_code} - {response.status_text} for URL: {response.url}")
            elif 500 <= status_code < 600:
                raise HTTPError(f"Server Error: {status_code} - {response.status_text} for URL: {response.url}")

        request.continue_().then(on_response)

    def set_page_url(self, p):
        self.page_url = p

    def fill(self, css_tag: str, value):
        e = self.locator_from_cache(css_tag)
        e.fill(value)
        return e

    def type(self, css_tag: str, value):
        e = self.locator_from_cache(css_tag)
        e.type(value)
        return e

    def press_enter(self):
        self.page.keyboard.press('Enter')

    def press(self, css_tag, v):
        e = self.locator_from_cache(css_tag)
        e.press(v)
        return e

    def enter(self, css_tag):
        e = self.locator_from_cache(css_tag)
        e.press("Enter")
        return e

    def click(self, css_tag):
        e = self.locator_from_cache(css_tag)
        e.click()
        return e

    def locator_from_cache(self, css_tag):
        if css_tag in self.cache:
            e = self.cache[css_tag]
        else:
            e = self.page.locator(css_tag)
            self.cache[css_tag] = e
        return e

    def run(self):
        pass

    def before_run(self):
        pass

    def after_run(self):
        self.browser.close()

    def wait_until(self, selector, timeout=10000):
        try:
            element = self.page.wait_for_selector(selector, timeout=timeout)
            return element
        except TimeoutError:
            raise TimeoutError(f"Element with selector '{selector}' did not appear within {timeout} ms")

    def main(self):
        with sync_playwright() as p:
            self.configure(p)
            self.before_run()
            self.page.goto(self.page_url)
            self.run()
            self.after_run()


def _main():
    b = Base()
    p = "p"
    b.set_page_url(p)
    b.main()


if __name__ == "__main__":
    _main()