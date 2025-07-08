import logging
import queue
import time
import threading
import sys
from collections import namedtuple

LogRow = namedtuple('LogRow', ['name', 'level', 'message'], defaults=['', 0, ''])



class BackgroundLogger:
    '''
    Фоновый логгер для асинхронной записи сообщений из нескольких потоков
    '''
    def __init__(self, name='', level=logging.DEBUG, queue_maxsize=1000):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self._queue = queue.Queue(maxsize=queue_maxsize)
        self._thread = threading.Thread(target=self._worker, daemon=True, name='logger')


    def _worker(self):
        try:
            logger = self.logger
            while True:
                row = self._queue.get()
                if row is None:
                    break

                try:
                    logger.log(row.level, f'[{row.name}] {row.message}')
                except Exception as ex:
                    self._dump_logger_error('BackgroundLogger logger error:', str(ex))

        except Exception as ex:
            self._dump_logger_error('BackgroundLogger worker error:', str(ex))


    def _dump_logger_error(self, caption, message):
        try:
            self.logger.error(f'{caption} {message}')
        except Exception as ex:
            print(f'[BackgroundLogger] {str(ex)}||{message}', file=sys.stderr, flush=True)


    def log(self, message, level=logging.INFO, source=None):
        row = LogRow(source or threading.current_thread().name
                     , level
                     , message)
        self._queue.put(row)

    def is_running(self):
        return self._thread.is_alive()

    def start(self):
        if self._thread.is_alive():
            raise RuntimeError("BackgroundLogger уже запущен")
        self._thread.start()

    def stop(self, timeout=None):
        if not self._thread.is_alive():
            return
        while not self._queue.empty():
            time.sleep(0.02)  # Ждём, пока очередь опустеет

        self._queue.put(None)
        self._thread.join(timeout)

    def addHandler(self, handler):
        self.logger.addHandler(handler)



