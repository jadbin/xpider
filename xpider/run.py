# coding=utf-8

import os
import signal
import logging

from xpider.config import DEFAULT_CONFIG
from xpider.crawler import Crawler
from xpider.utils import configure_logger, daemonize

log = logging.getLogger(__name__)


def run_spider(spider_factory, **kwargs):
    run_crawler(spider_factory, config=kwargs)


def run_crawler(spider_factory, config=None):
    c = dict(DEFAULT_CONFIG)
    if config is not None:
        c.update(config)
    config = c

    configure_logger('xpider', config)
    if config.get('daemon'):
        daemonize()
    pid_file = config.get('pid_file')
    _write_pid_file(pid_file)
    try:
        crawler = Crawler(config=config)
    except Exception:
        log.error('Failed to create crawler', exc_info=True)
        _remove_pid_file(pid_file)
        raise
    default_signal_handlers = _set_signal_handlers(crawler)
    try:
        crawler.run(spider_factory)
    finally:
        _remove_pid_file(pid_file)
        _recover_signal_handlers(default_signal_handlers)


def _write_pid_file(pid_file):
    if pid_file is not None:
        with open(pid_file, 'w') as f:
            f.write(str(os.getpid()))


def _remove_pid_file(pid_file):
    if pid_file is not None:
        try:
            os.remove(pid_file)
        except Exception as e:
            log.warning('Cannot remove PID file %s: %s', pid_file, e)


def _set_signal_handlers(crawler):
    def _exit(signum, frame):
        log.info('Received exit signal: %s', signum)
        crawler.stop()

    default_signal_handlers = [(signal.SIGINT, signal.getsignal(signal.SIGINT)),
                               (signal.SIGTERM, signal.getsignal(signal.SIGTERM))]
    signal.signal(signal.SIGINT, _exit)
    signal.signal(signal.SIGTERM, _exit)
    return default_signal_handlers


def _recover_signal_handlers(handlers):
    for h in handlers:
        signal.signal(h[0], h[1])
