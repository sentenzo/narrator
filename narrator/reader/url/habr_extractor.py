from bs4 import BeautifulSoup

from .base_url_extractor import BaseUrlExtractor
from narrator.article import Article


class HabrExtractor(BaseUrlExtractor):
    @staticmethod
    def extract_text(obj: str) -> str:
        html = BaseUrlExtractor.get_html(obj)
        soup = BeautifulSoup(html, "html.parser")
        article = Article()
        article["title"] = soup.select_one(
            "main h1[data-test-id='articleTitle'] span"
        ).text
        article["author"] = soup.select_one(
            "main a.tm-user-info__username"
        ).text.strip()
        article["date"] = soup.select_one("main div.tm-article-snippet__meta time").get(
            "title", ""
        )
        article.text.append(soup.select_one("#post-content-body p").text)

        return str(article)

    @staticmethod
    def is_extractable(obj: str) -> bool:
        re_temp = r"https\://habr\.com/../post/\d+"
        return BaseUrlExtractor._re_check_url(
            re_temp, obj
        ) and BaseUrlExtractor.is_extractable(obj)
