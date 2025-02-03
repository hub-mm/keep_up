# ./scripts/build_todo.py
class TodoBuild:
    todo_list = {}
    todo_counter = 0

    def __init__(self, task):
        self.task = task
        TodoBuild.todo_list[TodoBuild.todo_counter] =  self.task
        TodoBuild.todo_counter += 1

    @classmethod
    def delete_task(cls, task):
        try:
            values = list(cls.todo_list.values())
            values.remove(task)
            cls.todo_list = {i: v for i, v in enumerate(values)}
            cls.todo_counter = len(cls.todo_list)
        except ValueError:
            print('Task not found.')