

class Task:
    """
    A task, used to track and store information
    """

    def __init__(self, title, description=None, due_date=None, priority=None, tag=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.priority = priority
        self.tag = tag
