from data_classes import Assignment

class Player:
    def __init__(self, player_id):
        self.__player_id = player_id

        self.available = False
        self.__limits = set()
        self.__assignments = {}

        self.last_beg_time = None
        self.last_treat_time = None

        self.credits = 1

    def toggle_limit(self, limit_id: str):
        """Toggle presence of a given limit."""
        if limit_id in self.__limits:
            self.__limits.remove(limit_id)
        else:
            self.__limits.add(limit_id)

    def unset_limits(self):
        """Unset all limits."""
        self.__limits.clear()

    def assign_task(self, task_id: int, assigner_id: int):
        """Records an Assignment of a Task to a Player."""
        self.__assignments[task_id] = Assignment(task_id, assigner_id)

    def clear_assignments(self):
        """Clears all assignments."""
        self.__assignments.clear()

    def get_assignment(self, task_id: int):
        raise NotImplementedError
