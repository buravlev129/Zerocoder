import io
import logging
import pytest
import threading
import time
from queue import Empty
from libx.bglogger import BackgroundLogger
from libx.logf import get_line_formatter, get_console_handler, DATEFMT_SHORT


# Фикстура для создания временного потока для перехвата логов
@pytest.fixture
def log_stream():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    formatter = get_line_formatter(datefmt=DATEFMT_SHORT, level=True)
    handler.setFormatter(formatter)
    yield stream, handler
    handler.close()
    stream.close()

# Фикстура для создания BackgroundLogger
@pytest.fixture
def logger(log_stream):
    _, handler = log_stream
    lg = BackgroundLogger(level=logging.DEBUG, queue_maxsize=100)
    lg.addHandler(handler)
    yield lg
    if lg.is_running():
        lg.stop(timeout=1)


def test_initialization(log_stream):
    '''
    Проверяет корректность инициализации BackgroundLogger
    '''
    stream, handler = log_stream
    logger = BackgroundLogger(name='test_logger', level=logging.INFO, queue_maxsize=50)
    logger.addHandler(handler)
    
    assert logger.logger.name == 'test_logger'
    assert logger.logger.level == logging.INFO
    assert logger._queue.maxsize == 50
    assert logger._thread.daemon is True
    assert not logger.is_running()


def test_log_single_message(logger, log_stream):
    '''
    Проверяет запись одного сообщения в лог
    '''
    stream, _ = log_stream
    logger.start()
    
    logger.log("Test message", level=logging.INFO)
    time.sleep(0.1)  # Даём время обработать сообщение
    
    logger.stop()
    log_output = stream.getvalue()
    
    assert "INFO  [MainThread] Test message" in log_output


def test_log_multiple_threads(logger, log_stream):
    '''
    Проверяет запись сообщений из нескольких потоков
    '''
    stream, _ = log_stream
    messages = ["Message from thread 1", "Message from thread 2", "Message from thread 3"]

    def _worker(logger, msg):
        logger.log(msg, level=logging.DEBUG, source=f"worker-{threading.current_thread().name}")

    logger.start()

    threads = [
        threading.Thread(target=_worker, args=(logger, msg), name=f'thread-{i}') for i, msg in enumerate(messages)
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    
    time.sleep(0.5)
    logger.stop()

    log_output = stream.getvalue()
    assert f"DEBUG [worker-thread-" in log_output
    for msg in messages:
        assert msg in log_output


def test_multiple_start_stop(logger):
    '''
    Проверяет защиту от многократного запуска и остановки
    '''
    logger.start()
    with pytest.raises(RuntimeError, match="BackgroundLogger уже запущен"):
        logger.start()
    
    logger.stop()
    logger.stop()
    assert not logger.is_running()


def test_empty_queue_on_stop(logger, log_stream):
    '''
    Проверяет, что все сообщения обрабатываются перед остановкой
    '''
    stream, _ = log_stream
    messages = ["Message 1", "Message 2", "Message 3"]

    logger.start()
    for msg in messages:
        logger.log(msg, level=logging.INFO)

    logger.stop(timeout=1.0)
    assert logger._queue.qsize() == 0

    output_data = stream.getvalue()
    for msg in messages:
        assert msg in output_data


def test_worker_exception_handling(log_stream):
    '''
    Проверяет обработку исключений в логгере
    '''

    class BadHandler(logging.StreamHandler):
        def emit(self, record):
            raise ValueError('Simulated handler error')

    stream, handler = log_stream
    logger = BackgroundLogger(level=logging.DEBUG, queue_maxsize=10)
    logger.addHandler(handler)
    logger.addHandler(BadHandler())
    logger.start()

    logger.log('Test message', level=logging.INFO)

    time.sleep(0.2)
    logger.stop()

    stream_data = stream.getvalue()
    assert 'Simulated handler error' in stream_data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

