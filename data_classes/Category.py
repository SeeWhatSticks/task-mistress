from discord import Emoji

class Category:
    def __init__(self, category_id: str, emoji: Emoji, name: str):
        self.category_id = category_id
        self.emoji = emoji
        self.name = name
