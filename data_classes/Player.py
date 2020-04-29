import logging
from datetime import datetime
from data_classes.Assignment import Assignment

log = logging.getLogger(__name__)

class Player:
    def __init__(self, player_id):
        self._player_id = player_id

        self.available = False
        self.limits = set()
        self.assignments = {}

        self.last_beg_time = None
        self.last_treat_time = None

        self.credits = 1

    @classmethod
    def from_dict(cls, bot, d):
        player = Player(d['key'])
        player.available = d['available']
        player._limits = set(d['limits'])
        player.assignments = {v['key']: Assignment.from_dict(bot, v) for v in d['assignments']}
        if d['last_beg_time'] is None:
            player.last_beg_time = None
        else:
            player.last_beg_time = datetime.utcfromtimestamp(d['last_beg_time'])
        if d['last_treat_time'] is None:
            player.last_treat_time = None
        else:
            player.last_treat_time = datetime.utcfromtimestamp(d['last_treat_time'])
        player.credits = d['credits']
        return player

    def to_dict(self):
        return {
            'key': self._player_id,
            'available': self.available,
            'limits': list(self.limits),
            'assignments': [v.to_dict() for v in self.assignments],
            'last_beg_time': self.last_beg_time.timestamp(),
            'last_treat_time': self.last_treat_time.timestamp(),
            'credits': self.credits
        }

    def toggle_limit(self, limit_id: str):
        """Toggle presence of a given limit."""
        if limit_id in self.limits:
            self.limits.remove(limit_id)
        else:
            self.limits.add(limit_id)

    def unset_limits(self):
        """Unset all limits."""
        self.limits.clear()

    def assign_task(self, task_id: int, assigner_id: int):
        """Records an Assignment of a Task to a Player."""
        self.assignments[task_id] = Assignment(task_id, assigner_id)

    def clear_assignments(self):
        """Clears all assignments."""
        self.assignments.clear()

    def get_assignment(self, task_id: int):
        raise NotImplementedError
