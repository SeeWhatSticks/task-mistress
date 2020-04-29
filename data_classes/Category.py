import logging
from discord import Emoji

log = logging.getLogger(__name__)

class Category:
    def __init__(self, key: int, name: str, emoji: Emoji, description: str):
        self.key = key
        self.name = name

        self.emoji = emoji
        self.description = description

    @classmethod
    async def from_dict(cls, bot, d):
        return Category(
                d['key'],
                d['name'],
                await bot.fetch_emoji(d['emoji']),
                d['description']
        )

    def to_dict(self):
        return {
            'key': self.key,
            'name': self.name,
            'emoji': self.emoji.id,
            'self.description': self.description
        }

    @classmethod
    def from_dict(cls, bot, d):
        return cls(
            d['key'],
            d['name'],
            bot.get_emoji(d['emoji']),
            d['description'])
