# coding=utf-8

import logging

from xpider.context import DefaultContext
from xpider.request import Request

log = logging.getLogger(__name__)


class Spider:
    default_context_factory = DefaultContext

    def on_start(self):
        raise NotImplemented

    def crawl(self, url, driver=None, timeout=None, context=None, callback=None, errback=None, **kwargs):
        if context is None:
            context = self.default_context_factory()
        if driver:
            context.update_cookies(driver)
            context.update_local_storage(driver)
            context.update_session_storage(driver)
        if timeout is not None:
            context.timeout = timeout
        req = Request(url, context=context, callback=callback, errback=errback, **kwargs)
        self.crawler.push_request(req)

    @property
    def logger(self):
        return log

    def log(self, message, *args, level=logging.INFO, **kwargs):
        self.logger.log(level, message, *args, **kwargs)
