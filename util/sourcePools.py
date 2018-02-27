# -*- coding: utf-8 -*-


from concurrent.futures.thread import ThreadPoolExecutor
from concurrent.futures.process import ProcessPoolExecutor
from util.exception import SourcePoolException
from util.parseYaml import conf

class ThreadPool(object):
    def __call__(self):
        thread_pool = ThreadPoolExecutor(conf['threadPoolNum'])
        return thread_pool


class ProcessPool(object):
    """
    It must be a normal function ,not staticmethod or classmethod
    """
    def __call__(self):
        process_num = 2
        process_pool = ProcessPoolExecutor(process_num)
        return process_pool


class ExecutorPoolFactory(object):
    @staticmethod
    def create_pool(pool_type):
        if pool_type == 'io':
            return ThreadPool()()
        if pool_type == 'cpu':
            return ProcessPool()()
        raise SourcePoolException('No source type for this pool')