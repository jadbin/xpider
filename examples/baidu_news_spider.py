# coding=utf-8

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
