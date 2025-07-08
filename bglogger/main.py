import os
import threading
import time
import random

import libx.logf as logf
from libx.bglogger import BackgroundLogger
from logger_config import configure_logger


messages = [
        'Представим, что у нас',
        'есть несколько рабочих потоков,',
        'которые должны писать данные в общий лог',
        'Рабочие потоки сами',
        'не пишут в лог.',
        'Конец'
    ]


def worker(logger: BackgroundLogger):
    for msg in messages:
        delay = [0.3, 0.5, 0.2, 0.1]
        level = [logf.DEBUG, logf.ERROR, logf.ERROR, logf.WARNING]
        logger.log(msg, random.choice(level))
        time.sleep(random.choice(delay))


def init_logger():
    # p = os.path.dirname(__file__)
    p = os.path.abspath(os.getcwd())
    log_file = logf.prepare_logname_ver(os.path.join(p, 'Application'), 'x.y')

    lg = configure_logger(log_file, logf.DEBUG)
    return lg


if __name__ == '__main__':

    lg = init_logger()
    lg.start()

    threads = [threading.Thread(target=worker, args=(lg,), name=f'worker-{i}') for i in range(3)]
    for t in threads:
        t.start()

    for t in threads:
        t.join()


    #time.sleep(0.002)
    time.sleep(1)
    lg.stop()
    print('---')

