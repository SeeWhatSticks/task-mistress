import logging

log = logging.getLogger(__name__)

class Task:
    def __init__(self, task_id, task_text, task_name: None):
        self.task_id = task_id

        self.task_text = task_text
        self.task_name = task_name

        self.__categories = set()
        self.ratings = {}

        self.total_assignments = 0
        self.total_completions = 0

    def add_category(self, category_id):
        raise NotImplementedError

    def remove_category(self, category_id):
        raise NotImplementedError

    def toggle_category(self, limit_id: str):
        """Toggle presence of a given limit."""
        if limit_id in self.__categories:
            self.__categories.remove(limit_id)
        else:
            self.__categories.add(limit_id)

    def unset_categories(self):
        """Unset all categories."""
        self.__categories = self.categories.clear()

    def get_severity(self):
        """Calculate severity, based on the current severity ratings."""
        return "/5".format(round(sum(self.ratings.values())/len(self.ratings), 1))

    def get_completion_rate(self):
        """Calculate completion rate, based on total assignments and total completions."""
        return "{}%".format(round(self.total_completions/self.total_assignments, 2))
