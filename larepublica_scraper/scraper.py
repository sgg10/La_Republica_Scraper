import requests
import lxml.html as html

HOME_URL = "https://www.larepublica.co/"

XPATH = {
    "LINK_TO_ARTICLE": '//div[contains(@class, "V")]/a[contains(@class, "kicker")]/@href',
    "TITLE": '//div[@class="container title-share"]//h2/span/text()',
    "SUMMARY": '//div[@class="lead"]/p/text()',
    "BODY": '//div[@class="html-content"]/p[not(@class)]/text()'
}

def parse_home() -> None:
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode("utf-8")
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH['LINK_TO_ARTICLE'])
            print(links_to_notices)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve.message)

def run() -> None:
    parse_home()

if __name__ == '__main__':
    run()