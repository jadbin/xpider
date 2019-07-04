======
xpider
======

.. image:: https://travis-ci.org/jadbin/xpider.svg?branch=master
    :target: https://travis-ci.org/jadbin/xpider

.. image:: https://coveralls.io/repos/jadbin/xpider/badge.svg?branch=master
    :target: https://coveralls.io/github/jadbin/xpider?branch=master

.. image:: https://img.shields.io/badge/license-Apache 2-blue.svg
    :target: https://github.com/jadbin/xpider/blob/master/LICENSE

Spider Example
==============

以下是我们的一个爬虫类示例，其作用为爬取 `百度新闻 <http://news.baidu.com/>`_ 的热点要闻:

.. code-block:: python

    from xpider import Spider, run_spider


    class BaiduNewsSpider(Spider):
        def on_start(self):
            self.crawl('http://news.baidu.com/', callback=self.parse)

        def parse(self, req, driver):
            hot = driver.find_elements_by_css_selector('div.hotnews a')
            self.log("Hot News:")
            for i in range(len(hot)):
                self.log("%s: %s", i + 1, hot[i].text.strip())


    if __name__ == '__main__':
        run_spider(BaiduNewsSpider, log_level='debug')

Documentation
=============

http://xpider.readthedocs.io/
