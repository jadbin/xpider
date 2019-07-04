# coding=utf-8

import logging
from threading import Semaphore, Thread, Lock
import time

from xpider.config import DEFAULT_CONFIG
from xpider.utils import load_object

log = logging.getLogger(__name__)


class Crawler:
    def __init__(self, config=None):
        self.config = config or dict(DEFAULT_CONFIG)
        self.queue = None
        self.spider = None
        self._run_lock = None

    def run(self, spider_factory):
        self._init(spider_factory)
        t = Thread(target=self._run_spider)
        t.start()
        t.join()

    def _run_spider(self):
        self._busy = 0
        self._busy_lock = Lock()
        self.spider.on_start()
        st = Thread(target=self._supervisor_thread, daemon=True)
        st.start()
        for i in range(self.config.get('crawl_threads')):
            t = Thread(target=self._crawl_thread, daemon=True)
            t.start()
        self._run_lock = Semaphore(0)
        self._run_lock.acquire()
        self._run_lock = None
        self._busy_lock = None
        self._busy = None

    def _supervisor_thread(self):
        while True:
            time.sleep(5)
            with self._busy_lock:
                if self._busy == 0:
                    self.stop()

    def _crawl_thread(self):
        max_retry_times = self.config.get('max_retry_times')
        while True:
            req = self.queue.pop()
            retry = 0
            while retry <= max_retry_times:
                driver = None
                try:
                    log.debug('Get <%s>', req.url)
                    driver = req.context.create_web_driver()
                    driver.get(req.url)
                    log.debug('Get response of <%s>', req.url)
                except Exception as e:
                    log.warning('Failed to get <%s>: %s', req.url, e)
                else:
                    try:
                        req.callback(req, driver)
                    except Exception:
                        log.error('Error in callback', exc_info=True)
                    else:
                        break
                finally:
                    if driver is not None:
                        driver.quit()
                retry += 1
                log.debug('Retry <%s> (failed %s times)', req.url, retry)
            if retry > max_retry_times:
                if req.errback:
                    try:
                        req.errback(req)
                    except Exception:
                        log.error('Error in errback', exc_info=True)
            with self._busy_lock:
                self._busy -= 1
                if self._busy == 0:
                    self.stop()

    def push_request(self, req):
        with self._busy_lock:
            self._busy += 1
        self.queue.push(req)

    def stop(self):
        if self._run_lock:
            self._run_lock.release()

    def _init(self, spider_factory):
        self.queue = self._instance_from_crawler(self.config.get('queue_factory'))
        spider = self._instance_from_crawler(spider_factory)
        if not hasattr(spider, 'crawler'):
            spider.crawler = self
        self.spider = spider

    def _instance_from_crawler(self, factory):
        obj = load_object(factory)
        if hasattr(obj, 'from_crawler'):
            return obj.from_crawler(self)
        return obj()
