from datetime import datetime
import logging

log = logging.getLogger(__name__)

class Assignment:
    def __init__(self, task_id, assigner_id):
        self.task_id = task_id

        self.assigner = assigner_id
        self.assignment_time = datetime.utcnow()

        self.completed = False
        self.completion_time = None

        self.verifiers = []

    @classmethod
    def from_dict(cls, bot, d):
        assignment = Assignment(
                d['key'],
                d['assigner'])
        assignment.assignment_time = datetime.utcfromtimestamp(d['assignment_time'])
        assignment.completed = d['completed']
        assignment.verifiers = d['verifiers']
        return assignment

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'assigner': self.assigner,
            'assignment_time': self.assignment_time.timestamp(),
            'completed': self.completed,
            'completion_time': self.completion_time.timestamp(),
            'verifiers': self.verifiers
        }

    def mark_completed(self):
        """Mark an assignment as completed and record the completion time."""
        self.completed = True
        self.completion_time = datetime.utcnow()

    def add_verifier(self, verifier_id):
        """Record a verifier of a completed Assignment."""
        self.verifiers.append(verifier_id)
