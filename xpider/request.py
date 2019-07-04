# coding=utf-8


class Request:
    def __init__(self, url, context=None, callback=None, errback=None, **kwargs):
        self.url = url
        self.context = context
        self.callback = callback
        self.errback = errback
        for k, v in kwargs.items():
            setattr(self, k, v)
