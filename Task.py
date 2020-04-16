class Task:
    def __init__(self, task_id, task_text, task_name: None):
        self.task_id = task_id

        self.task_text = task_text
        self.task_name = task_name

        self.categories = []
        self.ratings = {}

        self.total_assignments = 0
        self.total_completions = 0
