import pickle
from data_classes import Player
from discord import Emoji

class PickledList:
    """A class that creates a dictionary and manages loading and saving the dictionary to a specified pickle file."""
    def __init__(self, bot, path):
        self.bot = bot
        self.__path = path
        self.__list = {}

        self.load_list()

    def save_list(self):
        """Pickle the list and save to a file."""
        pickle.dump(self.__list, open(self.__path, 'wb'))

    def load_list(self):
        """Load a file and unpickle the list."""
        try:
            self.__list = pickle.load(open(self.__path, 'rb'))
        except (OSError, pickle.PickleError):
            print("Error loading {}. Storing empty file.".format(self.__path))
            self.save_list()


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

    def get_player_by_id(self, user_id: int):
        """Return a Player for a given user_id. Adds the Player if not already in the PlayerList."""
        if user_id not in self.__list:
            self.__list[user_id] = Player(user_id)
        return self.__list[user_id]

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

    def cleanup_tasks(self):
        """Remove all deleted tasks."""
        raise NotImplementedError


class InterfaceList(PickledList):
    """Manages a dictionary mapping message_id to Interface."""

    def add_actionsinterface(self):
        raise NotImplementedError

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
