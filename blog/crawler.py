import re
from time import sleep
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests


class ClienNews(object):
    def __init__(self, name, url):
        self.id = None
        self.name = name
        self.url = url
        self.content = ''

        matched = re.search(r'wr_id=(\d+)', self.url)
        if matched:
            self.id = int(matched.group(1))
        else:
            raise ValueError('not found wr_id from {}'.format(self.url))

    def update_content(self):
        soup = self.get_page_soup(self.url)
        self.content = soup.select('#writeContents')[0].text

    @classmethod
    def get_page_soup(cls, url):
        response = requests.get(url)
        response.encoding = 'utf8'
        html = response.text
        return BeautifulSoup(html)

    @classmethod
    def get_news(cls, page=1):
        clien_news_url = "http://www.clien.net/cs2/bbs/board.php?bo_table=news&page={}".format(page)  # noqa
        soup = cls.get_page_soup(clien_news_url)

        for tr_tag in soup.select('.mytr'):
            try:
                link_tag = tr_tag.select('.post_subject a')[0]
            except IndexError:
                continue

            name = link_tag.text.strip()
            url = urljoin(clien_news_url, link_tag['href'])

            clien_news = ClienNews(name, url)
            clien_news.update_content()
            yield clien_news

            # break
            sleep(0.1)


if __name__ == '__main__':
    print('crawling ...')
    for clien_news in ClienNews.get_news():
        print('[{}] {}'.format(clien_news.id, clien_news.name))
