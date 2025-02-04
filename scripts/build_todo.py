# ./scripts/build_todo.py
import uuid


class TodoBuild:
    todo_list = {}
    todo_complete = {}

    def __init__(self, task):
        self.task = task
        self.id = uuid.uuid4()
        TodoBuild.todo_list[self.id] =  self.task

    @classmethod
    def delete_task(cls, task):
        found_key = None
        for key, val in cls.todo_list.items():
            if val == task:
                found_key = key
                break
        if found_key is not None:
            del cls.todo_list[found_key]
            return found_key
        else:
            print('Task not found.')
            return None

    @classmethod
    def delete_task_complete(cls, task):
        found_key = None
        for key, val in cls.todo_complete.items():
            if val == task:
                found_key = key
                break
        if found_key is not None:
            del cls.todo_complete[found_key]
            return found_key
        else:
            print('Task not found.')
            return None

    @classmethod
    def complete_task(cls, task):
        key = cls.delete_task(task)
        if key is not None:
            cls.todo_complete[key] = task
        else:
            print('Task not found.')