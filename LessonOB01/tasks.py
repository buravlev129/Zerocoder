
from typing import List


class Task:
    """
    Задача
    """

    def __init__(self, description, deadline):
        self.description = description
        self.deadline = deadline
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def __str__(self):
        status = "Выполнено" if self.completed else "Не выполнено"
        return f"Задача: {self.description}, Срок: {self.deadline}, Статус: {status}"


class TaskManager:
    """
    Менеджер задач
    """
    
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, description, deadline):
        task = Task(description, deadline)
        self.tasks.append(task)

    def mark_task_completed(self, index):
        if 0 <= index < len(self.tasks):
            self.tasks[index].mark_completed()

    def get_pending_tasks(self):
        return [task for task in self.tasks if not task.completed]

    def __str__(self):
        return "\n".join(str(task) for task in self.tasks)



if __name__ == "__main__":

    man = TaskManager()
    man.add_task("Купить продукты", "2023-10-10")
    man.add_task("Сделать домашнее задание", "2023-10-11")

    print("Все задачи:")
    print(man)

    man.mark_task_completed(0)

    print("\nТекущие задачи:")
    for task in man.get_pending_tasks():
        print(task)

