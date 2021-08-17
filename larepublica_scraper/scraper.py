import requests
import lxml.html as html
import os
import datetime

HOME_URL = "https://www.larepublica.co/"

XPATH = {
    "LINK_TO_ARTICLE": '//div[contains(@class, "V")]/a[contains(@class, "kicker")]/@href',
    "TITLE": '//div[@class="container title-share"]//h2/span/text()',
    "SUMMARY": '//div[@class="lead"]/p/text()',
    "BODY": '//div[@class="html-content"]/p[not(@class)]/text()'
}

def parse_notices(link, today):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            notice = response.content.decode("utf-8")
            parsed = html.fromstring(notice)

            try:
                title = parsed.xpath(XPATH['TITLE'])[0]
                title.replace('"', '')
                summary = parsed.xpath(XPATH['SUMMARY'])[0]
                body = parsed.xpath(XPATH['BODY'])
            except IndexError:
                return

            with open(f"larepublica_scraper/{today}/{title}.txt", "w", encoding="utf-8") as file:
                file.write(title)
                file.write("\n\n")
                file.write(summary)
                file.write("\n\n")
                for p in body:
                    file.write(p)
                    file.write("\n")
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve.message)

def parse_home() -> None:
    try:
        response = requests.get(HOME_URL)
        if response.status_code == 200:
            home = response.content.decode("utf-8")
            parsed = html.fromstring(home)
            links_to_notices = parsed.xpath(XPATH['LINK_TO_ARTICLE'])

            today = datetime.date.today().strftime("%d-%m-%Y")
            if not os.path.isdir(f"larepublica_scraper/{today}"):
                os.mkdir(f"larepublica_scraper/{today}")

            for link in links_to_notices:
                parse_notices(link, today)
        else:
            raise ValueError(f'Error: {response.status_code}')
    except ValueError as ve:
        print(ve.message)

def run() -> None:
    parse_home()

if __name__ == '__main__':
    run()