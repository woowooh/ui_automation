

def test_run(page_object):
    page_url = "https://www.baidu.com"
    page_object.set_page_url(page_url)
    page_object.page.goto(page_url)
    page_object.click_text("《哪吒2》总票房突破120亿", 0)

