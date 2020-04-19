import logging
import pickle
from data_classes.Player import Player
from data_classes.Task import Task
from data_classes.Interfaces import ActionsInterface, LimitsInterfaces, CategoriesInterface, AssignmentsInterface, \
    TasksInterface, VerificationInterface
from discord import Emoji, User

log = logging.getLogger(__name__)

class PickledList:
    """A class that creates a dictionary and manages loading and saving the dictionary to a specified pickle file."""
    def __init__(self, bot, path):
        self.bot = bot
        self.__path = path
        self.__list = {}

        self.load()

    def save(self):
        """Pickle the list and save to a file."""
        pickle.dump(self.__list, open(self.__path, 'wb'))

    def load(self):
        """Load a file and unpickle the list."""
        try:
            self.__list = pickle.load(open(self.__path, 'rb'))
        except (OSError, pickle.PickleError):
            log.warning("Error loading {}. Storing empty file.".format(self.__path))
            self.save()


class CategoryList(PickledList):
    """Manages a dictionary mapping category_id to Category."""

    def get_category_by_id(self, category_id: str):
        """Return the Category for a given category_id, or None."""
        raise NotImplementedError

    def get_category_by_emoji(self, emoji: Emoji):
        """Return the Category associated with a given Emoji, or None."""
        raise NotImplementedError


class PlayerList(PickledList):
    """Manages a dictionary mapping user_id to Player"""

    def get_player(self, user: User):
        """Return a Player for a given user_id. Adds the Player if not already in the PlayerList."""
        if user.id not in self.__list:
            self.__list[user.id] = Player(user.id)
        return self.__list[user.id]

    def get_available_players(self):
        """Return a dict mapping player_id to Player for Players who are marked as available."""
        return {k: v for (k, v) in self.__list.items() if v.available}

    def clear_assignments(self):
        """Clears all Assignments for all Players."""
        for player in self.__list:
            player.clear_assignments()


class TaskList(PickledList):
    """Manages a dictionary mapping task_id to Task."""

    def get_task_by_id(self, task_id: int):
        """Return a Task for a given task_id, or None."""
        if task_id in self.__list:
            return self.__list[task_id]
        return None

    def get_tasks_by_player(self, player_id: int):
        """Return a dict mapping task_id to Task for Tasks written by a given player."""
        raise NotImplementedError

    def get_tasks_for_player(self, player: Player):
        """Return a dict mapping task_id to Task for Tasks that are available for a given Player."""
        raise NotImplementedError

    def get_assigned_tasks_for_player(self, player: Player):
        """Returns a dict mapping task_id to Task for Tasks that are assigned to a given Player."""
        raise NotImplementedError

    def get_available_task_id(self):
        """Returns an available task_id."""
        task_id = 0
        while task_id in self.__list:
            task_id += 1
        return task_id

    def add_task(self, task_text: str, task_name: str = None):
        """Creates a new Task object and records it in the TaskList."""
        task_id = self.get_available_task_id()
        self.__list[task_id] = Task(task_id, task_text, task_name)

    def cleanup_tasks(self):
        """Remove all deleted tasks."""
        raise NotImplementedError


class InterfaceList(PickledList):
    """Manages a dictionary mapping message_id to Interface."""

    def add_actionsinterface(self, message_id: int):
        self.__list[message_id] = ActionsInterface(message_id)

    def add_limitsinterface(self):
        raise NotImplementedError

    def add_categoriesinterface(self):
        raise NotImplementedError

    def add_assignmentsinterface(self):
        raise NotImplementedError

    def add_tasksinterface(self):
        raise NotImplementedError

    def add_verificationinterface(self):
        raise NotImplementedError

    def get_interface_by_id(self, message_id: int):
        """Return an Interface for a given message_id, or None."""
        if message_id in self.__list:
            return self.__list[message_id]
        return None
