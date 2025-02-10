# ./scripts/build_todo.py
import uuid
import json
import os
import atexit


class TodoBuild:
    data_dir = 'json'
    data_file = os.path.join(data_dir, 'todo_data.json')

    todo_list = {}
    todo_complete = {}

    def __init__(self, task):
        self.task = task
        self.id = str(uuid.uuid4())
        TodoBuild.todo_list[self.id] = self.task

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

    @classmethod
    def edit_task(cls, task_id, new_value):
        try:
            task_uuid = uuid.UUID(task_id)
        except ValueError:
            print('Invalid task ID.')
            return
        if task_uuid in cls.todo_list:
            cls.todo_list[task_uuid] = new_value
        else:
            print('Task not found.')

    @classmethod
    def load_data(cls):
        if not os.path.exists(cls.data_dir):
            os.makedirs(cls.data_dir)

        if os.path.exists(cls.data_file):
            try:
                with open(cls.data_file, 'r') as f:
                    data = json.load(f)
                    cls.todo_list = data.get('todo_list', {})
                    cls.todo_complete = data.get('todo_complete', {})
                print('Todo data loaded successfully.')
            except Exception as e:
                print(f"Error loading data: {e}")
        else:
            cls.todo_list = {}
            cls.todo_complete = {}

    @classmethod
    def save_data(cls):
        if not os.path.exists(cls.data_dir):
            os.makedirs(cls.data_dir)

        data = {
            'todo_list': cls.todo_list,
            'todo_complete': cls.todo_complete,
        }

        try:
            with open(cls.data_file, 'w') as f:
                json.dump(data, f)
            print('Todo data saved successfully.')
        except Exception as e:
            print(f"Error saving data: {e}")


atexit.register(TodoBuild.save_data)
TodoBuild.load_data()
