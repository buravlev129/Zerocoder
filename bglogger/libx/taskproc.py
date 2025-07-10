import queue
import time
import threading
import sys
from concurrent.futures import ThreadPoolExecutor, Future
from typing import Any, Optional
from enum import Enum


class TaskState(Enum):
    Unknown = 0
    Running = 1
    Done = 2
    Cancelled = 3
    Error = 4


class Task:
    def __init__(self, key: str, data: Any = None):
        self.key = key
        self.data = data
        self.future: Optional[Future] = None
        self.result: Optional[Any] = None
        self.exception: Optional[Exception] = None
        self.state:TaskState = TaskState.Unknown
        self.sender: str = ''

    def execute(self):
        return f'{self.key}'
    
    def __repr__(self):
        return f'{self.key} {self.state}'


class TaskProcessor:
    def __init__(self, queue_size=0, max_workers=5, prefix=''):
        self._queue = queue.Queue(maxsize=queue_size)
        self._results: dict[str, Task] = {}
        self._lock = threading.Lock()
        self._shutdown = False

        self._executor = ThreadPoolExecutor(max_workers=max_workers, thread_name_prefix=prefix)
        self._worker_thread = threading.Thread(target=self._loop, daemon=True, name='worker_thread')
        self._worker_thread.start()


    def _loop(self):
        try:
            while True:
                task = self._queue.get()
                if task is None:
                    break

                with self._lock:
                    task.future = self._executor.submit(self._execute_task, task)
                    self._results[task.key] = task
                    
                self._queue.task_done()
        except Exception as ex:
            print(f'[TaskProcessor] {str(ex)}', file=sys.stderr)

    def _execute_task(self, task):
        try:
            result = task.execute()
            task.result = result
            task.state = TaskState.Done
        except Exception as ex:
            task.exception = ex
            task.state = TaskState.Error


    def stop(self, timeout=None):
        '''
        Останавливает работу TaskProcessor. Завершает все задачи в очереди, если есть
        '''
        if not self._worker_thread.is_alive():
            return
        with self._lock:
            self._shutdown = True

        while not self._queue.empty():
            time.sleep(0.02)  # Ждём, пока очередь опустеет

        self._queue.put(None)
        self._worker_thread.join(timeout)
        self._executor.shutdown(wait=True)

    def shutdown(self, timeout=None):
        '''
        Прерывает работу TaskProcessor. Отбрасывает все оставшиеся в очереди задачи
        '''
        if not self._worker_thread.is_alive():
            return
        
        with self._lock:
            self._shutdown = True

        self._queue.put(None)
        self._worker_thread.join(timeout)
        self._executor.shutdown(wait=True, cancel_futures=True)


    def add(self, task: Task):
        with self._lock:
            if not self._shutdown:
                self._queue.put(task)

    def add_range(self, tasks: list[Task]):
        with self._lock:
            if self._shutdown:
                return
            for t in tasks:
                self._queue.put(t)

    def pop(self, key) -> Task|None:
        '''
        Удаляет задачу с указанным ключом key. Возвращает значение, связанное с этим ключом
        '''
        with self._lock:
            if key in self._results:
                return self._results.pop(key, None)
        return None

    def popitem(self) -> Task|None:
        '''
        Удаляет из списка и возвращает последнюю добавленную задачу
        '''
        with self._lock:
            if self._results:
                return self._results.popitem()[1]
        return None

    def get_status(self, key):
        '''
        Возвращает статус указанной задачи
        '''
        with self._lock:
            if key in self._results:
                return self._results[key].state
        return TaskState.Unknown
