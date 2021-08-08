import unittest

from spider.parse import get_article_by_search, get_article_detail


class TestParse(unittest.TestCase):
    def test_parse_article_list(self):
        with open("./file/article_list.html", encoding='utf-8') as f:
            article_list = get_article_by_search(f.read())
        for item in article_list:
            print(item)

    def test_parse_article_detail(self):
        with open("./file/article_detail.html", encoding='utf-8') as f:
            article_detail = get_article_detail(f.read())
        for key, value in article_detail.items():
            print(key+":"+str(value))


if __name__ == '__main__':
    unittest.main()
