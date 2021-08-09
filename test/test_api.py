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

    def test_parse_article_detail(self):
        url = 'https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS8t07-lxV2_B-U8bJvyPmGe0hcU0-Yu4HVqXa8Fplpd9pTtTR0biH9eXcCpkNTK0Y6wDlhxa6zKUSU-74juxY-FC5DGv83XWVpptNeFbQerNNAvZ7OC0VhEE7yDiY4Q5DGpCIQ54OtPjonZYpmbvARJULy3ozEd2JbWxIIYI7qXjhp4vxnHsXh4JJaDz_ddlVF-qt7Z6k47Hcso-qdD84pjvzHZXxeLdyg..&type=2&query=%E5%90%B4%E7%AD%BE&token=8306C5021FE365141A1FD310AFBA3AD21BEF40D0610FC22C'
        article_detail = self.spider.get_article_content(url)
        for key, value in article_detail.dict().items():
            print(key + ":" + str(value))


if __name__ == '__main__':
    unittest.main()
