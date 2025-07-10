import pytest
import time
import threading
from random import choice
from concurrent.futures import ThreadPoolExecutor
from libx.taskproc import TaskProcessor, Task, TaskState


@pytest.fixture()
def task_processor():
    processor = TaskProcessor(queue_size=8, max_workers=4, prefix='pool_worker')
    yield processor
    processor.shutdown()

def create_task(key, delay=0.0):
    t = Task(key, data=[1,2,3])

    def execute():
        time.sleep(delay)
        return f'results for {key}'
    
    t.execute = execute
    return t


def test_single_task_execution(task_processor):
    '''
    Проверяем, что задача успешно добавляется, выполняется и возвращает результат
    '''
    t = create_task('k22', 0.2)
    task_processor.add(t)

    time.sleep(0.3)
    assert task_processor.get_status(t.key) == TaskState.Done
    assert t.result == f'results for {t.key}'


def test_single_task_execution_2(task_processor):
    '''
    Проверяем, что задача успешно добавляется, выполняется и возвращает результат
    '''
    class T2(Task):
        def execute(self):
            time.sleep(0.3)
            lst = [str(x*x) for x in self.data]
            return f'{self.key}: ' + ', '.join(lst)

    t = T2('k119', data=[3,4,3])
    task_processor.add(t)
    time.sleep(0.3)
    
    if t.future:
        t.future.result()  # Блокируем выполнение до завершения задачи

    assert t.state == TaskState.Done
    assert t.result == f'{t.key}: 9, 16, 9'


def test_single_task_catch_error(task_processor):
    '''
    Проверяем перехват исключений при обрабтке задачи
    '''
    class T2(Task):
        def execute(self):
            time.sleep(0.1)
            raise ValueError(f'{self.key} ОШИБКА')

    t = T2('k119')
    task_processor.add(t)
    time.sleep(0.3)

    if t.future:
        t.future.result()

    assert t.state == TaskState.Error
    assert f'{t.key} ОШИБКА' in str(t.exception)


def test_cancellation_task(task_processor):
    '''
    Проверяем, что при вызове `shutdown` неначатые задачи будут отменены
    '''
    tasks = [create_task(f'k2{i}', 1.2) for i in range(1, 7) ]
    task_processor.add_range(tasks[0:4])
    time.sleep(0.2)
    task_processor.add_range(tasks[4:6])

    task_processor.shutdown()
    time.sleep(2)
    for t in tasks[0:4]:
        assert t.state == TaskState.Done

    for t in tasks[4:]:
        assert t.state == TaskState.Unknown
        assert t.future is not None
        assert t.future.cancelled() == True


def test_concurrent_task_addition(task_processor):
    '''
    Проверяем, что задачи корректно добавляются и выполняются из нескольких потоков
    '''
    delays = [0.5, 0.6, 0.2, 0.3, 0.8, 0.8]
    keys = [f"task{i}" for i in range(1, 16)]

    def add_task(key, delay):
        t = create_task(key, delay) 
        task_processor.add(t)

    threads = []
    for key in keys:
        duration = choice(delays)
        th = threading.Thread(target=add_task, args=(key, duration,), name='source')
        threads.append(th)
        th.start()

    for th in threads:
        th.join()

    task = task_processor.popitem()
    while task:
        task.future.result()
        print(f'{task.key} -> {task.state}')
        assert task.state == TaskState.Done
        task = task_processor.popitem()


def test_high_load(task_processor):
    num_tasks = 100
    keys = [f"task{i}" for i in range(num_tasks)]

    def add_and_check_task(key):
        task = create_task(key, delay=0.01)
        task_processor.add(task)

        time.sleep(0.05)
        assert task_processor.get_status(key) == TaskState.Done

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(add_and_check_task, key) for key in keys]

    for future in futures:
        future.result()




if __name__ == "__main__":
    pytest.main([__file__, "-v"])

