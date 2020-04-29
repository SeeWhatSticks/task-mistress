import logging
from datetime import datetime

from discord import User

log = logging.getLogger(__name__)

class Task:
    def __init__(self, task_id: int, creator_id: int, task_text: str, task_name: str):
        self.task_id = task_id
        self.creator_id = creator_id
        self.creation_time = datetime.utcnow()

        self.task_text = task_text
        self.task_name = task_name

        self.categories = set()
        self.ratings = {}

        self.total_assignments = 0
        self.total_completions = 0

    @classmethod
    def from_dict(cls, bot, d):
        task = Task(d['key'], d['creator_id'], d['task_text'], d['task_name'])
        task.creation_time = datetime.utcfromtimestamp(d['creation_time'])
        task.categories = set(d['categories'])
        task.ratings = d['ratings'],
        task.total_assignments = d['total_assignments']
        task.total_completions = d['total_completions']
        return task

    def to_dict(self):
        return {
            'key': self.task_id,
            'creator_id': self.creator_id,
            'creation_time': self.creation_time.timestamp(),
            'task_text': self.task_text,
            'task_name': self.task_name,
            'categories': list(self.categories),
            'ratings': self.ratings,
            'total_assignments': self.total_assignments,
            'total_completions': self.total_completions
        }

    def add_category(self, category_id):
        raise NotImplementedError

    def remove_category(self, category_id):
        raise NotImplementedError

    def toggle_category(self, limit_id: str):
        """Toggle presence of a given limit."""
        if limit_id in self.categories:
            self.categories.remove(limit_id)
        else:
            self.categories.add(limit_id)

    def unset_categories(self):
        """Unset all categories."""
        self.categories.clear()

    def add_rating(self, user: User, rating: int):
        self.ratings[user.id] = rating

    def assigned(self):
        """Mark that the Task was assigned, keeping a running total."""
        self.total_assignments += 1

    def completed(self):
        """Mark that the Task was completed, keeping a running total."""
        self.total_completions += 1

    def get_severity(self):
        """Calculate severity, based on the current severity ratings."""
        return "{}/5".format(round(sum(self.ratings.values())/len(self.ratings), 1))

    def get_completion_rate(self):
        """Calculate completion rate, based on total assignments and total completions."""
        return "{}%".format(round(self.total_completions/self.total_assignments, 2))
