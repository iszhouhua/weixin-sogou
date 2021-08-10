import unittest

from spider.spider import Spider


class TestParse(unittest.TestCase):
    def setUp(self):
        self.spider = Spider()

    def test_search_article(self):
        keyword = '吴签'
        article_list = self.spider.search(keyword, 1)
        for item in article_list:
            print(item.dict())

    def test_get_article_detail(self):
        url = 'https://mp.weixin.qq.com/s?src=11&timestamp=1628559731&ver=3243&signature=qdq1vBIxIyEUrCAnruMAzKaXzQVKuZx-NJisnScIQubN6V634BNaXGtM6PybJrOPKfY3m898HPIkREXP5HQJ41ZMGidChCLbWaOutUaFn5ZjQQ341p0RYmLoG8uE3cJl&new=1'
        article_detail = self.spider.get_detail(url)
        for key, value in article_detail.dict().items():
            print(key + ":" + str(value))

    def test_search_profile(self):
        keyword = '吴签'
        profile_list = self.spider.search(keyword, 1, 1)
        for item in profile_list:
            print(item.dict())

    def test_get_profile_detail(self):
        url = 'http://mp.weixin.qq.com/profile?src=3&timestamp=1628559966&ver=1&signature=cHAScjG2Q34-O7n224wwOirQhCRCB7Zfe2WVTQ1Iy9SNe1FID9CWrHzNH-IIbJONNOHuDdywY-ceayQJk1e3Og=='
        profile_detail = self.spider.get_detail(url, 1)
        for key, value in profile_detail.dict().items():
            print(key + ":" + str(value))


if __name__ == '__main__':
    unittest.main()
