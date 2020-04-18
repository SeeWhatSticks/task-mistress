from discord import Embed, Emoji, Member, Reaction
from discord import NotFound, Forbidden, HTTPException

class Interface:
    """
    Base Interface class.
    Provides methods for interacting with the elements that implement Interfaces.
    An Interface always references a Discord Embed in a Message.
    An Interface typically has a number of Reactions that act as buttons.
    """
    def __init__(self, bot, message_id: int):
        self.bot = bot
        self.message_id = message_id
        self.pages = False
        self.page = 0

    async def get_message(self):
        # TODO: Can throw (NotFound, Forbidden, HTTPException)
        return await self.bot.fetch_message(self.message_id)

    async def update(self, embed: Embed):
        message = await self.get_message()
        # TODO: Can throw (Forbidden, HTTPException)
        await message.edit(embed=embed)

    async def delete(self):
        message = await self.get_message()
        # TODO: Can throw (Forbidden, NotFound, HTTPException)
        await message.delete()

    async def add_button(self, emoji: Emoji):
        message = await self.get_message()
        # TODO: Can throw (HTTPException, Forbidden, NotFound, InvalidArgument)
        await message.add_reaction(emoji)

    async def clear_buttons(self):
        message = await self.get_message()
        # TODO: Can throw (Forbidden, HTTPException)
        await message.clear_reactions()

    async def remove_button_press(self, emoji: Emoji, member: Member):
        message = await self.get_message()
        # TODO: Can throw (HTTPException, Forbidden, NotFound, InvalidArgument)
        await message.remove_reaction(emoji, member)

    async def handle_click(self):
        pass


class ActionsInterface(Interface):
    """Interface for various one-click game actions."""
    def __init__(self, bot, message_id: int):
        super().__init__(bot, message_id)


class LimitsInterfaces(Interface):
    """Interface for setting Player limits."""
    def __init__(self, bot, message_id: int, player_id: int):
        super().__init__(bot, message_id)

        self.player_id = player_id


class CategoriesInterface(Interface):
    """Interface for setting Task categories."""
    def __init__(self, bot, message_id: int, task_id: int):
        super().__init__(bot, message_id)

        self.task_id = task_id


class AssignmentsInterface(Interface):
    """Interface for viewing Player Assignments."""
    def __init__(self, bot, message_id: int, player_id: int):
        super().__init__(bot, message_id)

        self.player_id = player_id


class TasksInterface(Interface):
    """Interface for viewing Player Tasks (as in, user created Tasks)."""
    def __init__(self, bot, message_id: int, player_id: int):
        super().__init__(bot, message_id)

        self.player_id = player_id


class VerificationInterface(Interface):
    """Interface for verifying Task completion."""
    def __init__(self, bot, message_id: int, player_id: int, task_id: int):
        super().__init__(bot, message_id)

        self.player_id = player_id
        self.task_id = task_id
