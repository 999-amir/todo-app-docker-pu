""" this file will add day, month, level to session and then used for create new task in .views """
TODO_TASK_SESSION_ID = 'todo_task'


class TodoTaskSession:
    def __init__(self, request):
        self.session = request.session
        todo_task = self.session.get(TODO_TASK_SESSION_ID)
        if not todo_task:
            self.session[TODO_TASK_SESSION_ID] = {}
        self.todo_task = self.session[TODO_TASK_SESSION_ID]

    def add_day(self, day):
        self.todo_task['day'] = day
        self.save()

    def add_month(self, month):
        self.todo_task['month'] = month
        self.save()

    def add_level(self, level):
        self.todo_task['level'] = level
        self.save()

    def clear_session(self):
        self.session[TODO_TASK_SESSION_ID] = {}
        self.save()

    def save(self):
        self.session.modified = True
