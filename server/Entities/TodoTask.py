class TodoTask:
    _id_counter = 1

    def __init__(self, task_name):
        self.validate(task_name)
        self._task_name = task_name
        self._id = str(TodoTask._id_counter)
        TodoTask._id_counter += 1

    def get_id(self):
        return self._id

    def get_task_name(self):
        return self._task_name

    def update_task(self, task):
        self.validate(task)
        self._task_name = task

    def validate(self, task_name):
        if task_name is None or task_name.strip() == '':
            raise ValueError("task name cannot be empty")
