import logging
from discord import Embed, Emoji, Member, Message, Reaction
from discord import NotFound, Forbidden, HTTPException

log = logging.getLogger(__name__)

SYMBOLS = {
    'CHECK_MARK': "\U00002705",
    'RATINGS': {
        '1\U0000FE0F\U000020E3': 1,
        '2\U0000FE0F\U000020E3': 2,
        '3\U0000FE0F\U000020E3': 3,
        '4\U0000FE0F\U000020E3': 4,
        '5\U0000FE0F\U000020E3': 5
    },
    'BACK_ARROW': "\U000025C0\U0000FE0F",
    'FWRD_ARROW': "\U000025B6\U0000FE0F",
    'REFRESH': "\U0000267B\U0000FE0F",
    'DELETE': "\U0001F5D1\U0000FE0F",
    'AVAILABLE': "\U00002600\U0000FE0F",
    'UNAVAILABLE': "\U0001F319",
    'UNSET_LIMITS': "\U0001F3F4\U0000200D\U00002620\U0000FE0F",
    'SET_LIMITS': "\U0001F3F3\U0000FE0F",
    'BEG': "\U0001F3B0"
}
COLORS = {
    'default': 0x3300cc,
    'set': 0x003399,
    'verify': 0xff3399,
    'confirm': 0x33ff33,
    'error': 0xff3333
}

class Interface:
    """
    Base Interface class.
    Provides methods for interacting with the elements that implement Interfaces.

    An Interface always references a Discord Embed in a Message.
    An Interface typically has a number of Reactions that act as buttons.

    Most Interface class methods allow an optional Message parameter to reduce API calls to fetch the same message.
    """
    def __init__(self, bot, message_id: int):
        self.bot = bot
        self.message_id = message_id
        self.pages = False
        self.page = 0

    async def get_message(self):
        # TODO: Can throw (NotFound, Forbidden, HTTPException)
        return await self.bot.fetch_message(self.message_id)

    async def update(self, embed: Embed, message: Message = None):
        if message is None:
            message = await self.get_message()
        # TODO: Can throw (Forbidden, HTTPException)
        await message.edit(embed=embed)

    async def delete(self, message: Message = None):
        if message is None:
            message = await self.get_message()
        # TODO: Can throw (Forbidden, NotFound, HTTPException)
        await message.delete()

    async def add_button(self, emoji: Emoji, message: Message = None):
        if message is None:
            message = await self.get_message()
        # TODO: Can throw (HTTPException, Forbidden, NotFound, InvalidArgument)
        await message.add_reaction(emoji)

    async def clear_buttons(self, message: Message = None):
        if message is None:
            message = await self.get_message()
        # TODO: Can throw (Forbidden, HTTPException)
        await message.clear_reactions()

    async def remove_button_press(self, emoji: Emoji, member: Member, message: Message = None):
        if message is None:
            message = await self.get_message()
        # TODO: Can throw (HTTPException, Forbidden, NotFound, InvalidArgument)
        await message.remove_reaction(emoji, member)

    async def build_embed(self):
        """Create the Embed object for this Interface."""
        raise NotImplementedError

    async def handle_click(self):
        raise NotImplementedError


class ActionsInterface(Interface):
    """Interface for various one-click game actions."""
    def __init__(self, bot, message_id: int):
        super().__init__(bot, message_id)

    def build_embed(self):
        embed = Embed(
                title="Action Buttons",
                description="Have some buttons that do different things:",
                color=COLORS['default'])
        embed.add_field(
                name="{} Mark as available".format(SYMBOLS['AVAILABLE']),
                value="Marks you as available to have tasks assigned to you by TaskMistress, or by other players.")
        embed.add_field(
                name="{} Mark as unavailable".format(SYMBOLS['UNAVAILABLE']),
                value="Marks you as not available to receive assignments.")
        embed.add_field(
                name="{} Unset limits".format(SYMBOLS['UNSET_LIMITS']),
                value="Clears all of your limits.")
        embed.add_field(
                name="{} Set limits".format(SYMBOLS['SET_LIMITS']),
                value="Provides an interface for setting your limits.")
        embed.add_field(
                name="{} Beg".format(SYMBOLS['BEG']),
                value="Request an assignment from TaskMistress.")
        return embed

    async def add_buttons(self, message: Message = None):
        if message is None:
            message = self.get_message()
        await message.add_button(SYMBOLS['AVAILABLE'], message=message)
        await message.add_button(SYMBOLS['UNAVAILABLE'], message=message)
        await message.add_button(SYMBOLS['UNSET_LIMITS'], message=message)
        await message.add_button(SYMBOLS['SET_LIMITS'], message=message)
        await message.add_button(SYMBOLS['BEG'], message=message)


class LimitsInterfaces(Interface):
    """Interface for setting Player limits."""
    def __init__(self, bot, message_id: int, player_id: int):
        super().__init__(bot, message_id)

        self.player_id = player_id

    async def build_embed(self):
        user = await self.bot.fetch_user(self.player_id)
        player = self.bot.player_list.get_player_by_id(self.player_id)
        embed = Embed(
                title="Limits for {}".format(user.display_name),
                description="Click the buttons below to toggle your limits.",
                color=COLORS['default'])
        # TODO: For limit in player's limits, add field describing limit.
        return embed

    def add_buttons(self):
        pass


class CategoriesInterface(Interface):
    """Interface for setting Task categories."""
    def __init__(self, bot, message_id: int, task_id: int):
        super().__init__(bot, message_id)

        self.task_id = task_id

    def build_embed(self):
        task = self.bot.player_list.get_player_by_id(self.task_id)
        embed = Embed(
                title="Limits for {} ({})".format(task.name, task.id),
                description="Click the buttons below to toggle task categories.",
                color=COLORS['default'])
        # TODO: For category in task's categories, add field describing category.
        return embed


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
