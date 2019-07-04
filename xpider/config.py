# coding=utf-8

from os import cpu_count

DEFAULT_CONFIG = {
    'daemon': False,
    'log_level': 'info',
    'log_format': '%(asctime)s %(name)s [%(levelname)s] %(message)s',
    'log_dateformat': '[%Y-%m-%d %H:%M:%S %z]',
    'queue_factory': 'xpider.queue.FifoQueue',
    'crawl_threads': 4 * cpu_count(),
    'max_retry_times': 3
}
