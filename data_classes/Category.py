import logging
from discord import Emoji

log = logging.getLogger(__name__)

class Category:
    def __init__(self, category_id: str, name: str, emoji: Emoji, description: str):
        self.category_id = category_id
        self.name = name

        self.emoji = emoji
        self.description = description
