import json
import logging
from typing import Any, Coroutine

import data_classes.Interfaces as Interfaces
from data_classes.Category import Category
from data_classes.Player import Player
from data_classes.Task import Task
from discord import Emoji, User, Message
from discord.abc import Messageable

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(logging.DEBUG)

class CannedDict:
    """A class that creates a dictionary and manages loading and saving the dictionary to a specified file."""
    def __init__(self, bot, path):
        self.bot = bot
        self._path = path
        self._list = {}

        self.load(bot)

    def __contains__(self, key):
        return key in self._list

    def __getitem__(self, key):
        return self._list[key]

    def save(self):
        """Serialize the list and save to a file."""
        json.dump(
                [v.to_dict() for v in self._list.values()],
                open(self._path, 'w'))

    def has_key(self, key):
        """Returns True if key is present in list."""
        return key in self._list

    def get_value(self, key):
        return self._list[key]

    def get_available_key(self):
        """Returns an available integer key."""
        key = 0
        while key in self._list:
            key += 1
        return key

    def values(self):
        return self._list.values()


class CategoryList(CannedDict):
    """Manages a dictionary mapping category_id to Category."""

    def load(self, bot):
        """Load a file and deserialize the list."""
        self._list = {v['key']: Category.from_dict(bot, v) for v in json.load(open(self._path, 'r'))}

    def get_category_by_emoji(self, emoji: Emoji):
        """Return the Category associated with a given Emoji, or None."""
        raise NotImplementedError

    def add(self, name, emoji, description):
        """Creates a category object and adds it to the dictionary. Returns (key, Category)."""
        key = self.get_available_key()
        category = Category(key, name, emoji, description)
        self._list[key] = category
        self.save()
        return key, category

class PlayerList(CannedDict):
    """Manages a dictionary mapping user_id to Player"""

    def load(self, bot):
        """Load a file and deserialize the list."""
        self._list = {v['key']: Player.from_dict(bot, v) for v in json.load(open(self._path, 'r'))}

    def get_player(self, user: User):
        """Return a Player for a given user_id. Adds the Player if not already in the PlayerList."""
        if user.id not in self._list:
            self._list[user.id] = Player(user.id)
            self.save()
        return self._list[user.id]

    def get_available_players(self):
        """Return a dict mapping player_id to Player for Players who are marked as available."""
        return {k: v for (k, v) in self._list.items() if v.available}

    def clear_assignments(self):
        """Clears all Assignments for all Players."""
        for player in self._list:
            player.clear_assignments()


class TaskList(CannedDict):
    """Manages a dictionary mapping task_id to Task."""

    def load(self, bot):
        """Load a file and deserialize the list."""
        self._list = {v['key']: Task.from_dict(bot, v) for v in json.load(open(self._path, 'r'))}

    def get_tasks_by_player(self, player_key: int):
        """Return a dict mapping task_key to Task for Tasks written by a given Player."""
        raise NotImplementedError

    def get_tasks_for_player(self, player: Player):
        """Return a dict mapping task_key to Task for Tasks that are available for a given Player."""
        raise NotImplementedError

    def get_assigned_tasks_for_player(self, player: Player):
        """Returns a dict mapping task_key to Task for Tasks that are assigned to a given Player."""
        raise NotImplementedError

    def add_task(self, task_text: str, task_name: str = None):
        """Creates a new Task object and records it in the TaskList."""
        key = self.get_available_key()
        task = Task(key, task_text, task_name)
        self._list[key] = task
        return key, task

    def cleanup_tasks(self):
        """Remove all deleted tasks."""
        raise NotImplementedError


class InterfaceList(CannedDict):
    """Manages a dictionary mapping message_id to Interface."""

    def load(self, bot):
        """Load a file and deserialize the list"""
        self._list = {v['key']: Interfaces.Interface.from_dict(bot, v) for v in json.load(open(self._path, 'r'))}

    async def add_actions_interface(self, channel: Messageable):
        interface = Interfaces.ActionsInterface(self.bot)
        message = await interface.post(channel)
        self._list[message.id] = interface
        self.save()
        await interface.add_buttons(message=message)
        return message.id, interface

    async def add_category_info_interface(self, channel: Messageable):
        interface = Interfaces.CategoryInfoInterface(self.bot)
        message = await interface.post(channel)
        self._list[message.id] = interface
        self.save()
        await interface.add_buttons(message=message)
        return message, interface

    def add_limits_interface(self):
        raise NotImplementedError

    def add_categories_interface(self):
        raise NotImplementedError

    def add_assignments_interface(self):
        raise NotImplementedError

    def add_tasks_interface(self):
        raise NotImplementedError

    def add_verification_interface(self):
        raise NotImplementedError
