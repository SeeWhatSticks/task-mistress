import logging
from discord import Emoji

log = logging.getLogger(__name__)

class Category:
    def __init__(self, category_id: str, emoji: Emoji, name: str):
        self.category_id = category_id
        self.emoji = emoji
        self.name = name
