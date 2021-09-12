import unittest

from app.spider.parse import *


class TestParse(unittest.TestCase):
    def test_parse_article_list(self):
        with open("./file/article_list.html", encoding='utf-8') as f:
            article_list = get_article_by_search(f.read())
        for item in article_list:
            print(item)

    def test_parse_profile_list(self):
        with open("file/profile_list.html", encoding='utf-8') as f:
            gzh_list = get_profile_by_search(f.read())
        for item in gzh_list:
            print(item)

    def test_parse_article_detail(self):
        with open("./file/article_detail.html", encoding='utf-8') as f:
            article_detail = get_article_detail(f.read())
        for key, value in article_detail.dict().items():
            print(key + ":" + str(value))

    def test_parse_profile_detail(self):
        with open("file/profile_detail.html", encoding='utf-8') as f:
            profile_detail = get_profile_detail(f.read())
        for key, value in profile_detail.dict().items():
            print(key + ":" + str(value))


if __name__ == '__main__':
    unittest.main()
