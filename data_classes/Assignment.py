from datetime import datetime

class Assignment:
    def __init__(self, task_id, assigner_id):
        self.task_id = task_id

        self.assigner = assigner_id
        self.assignment_time = datetime.utcnow()

        self.completed = False
        self.completion_time = None

        self.verifiers = []

    def mark_completed(self):
        """Mark an assignment as completed and record the completion time."""
        self.completed = True
        self.completion_time = datetime.utcnow()

    def add_verifier(self, verifier_id):
        """Record a verifier of a completed Assignment."""
        self.verifiers.append(verifier_id)
