import json
import logging
import typing
from data_classes.Lists import CategoryList, PlayerList, TaskList, InterfaceList
from discord import Embed,      Emoji, Member
from discord.ext import commands

log = logging.getLogger(__name__)
logging.basicConfig()
log.setLevel(logging.DEBUG)

CONFIG_FILE = "config.json"
CATEGORY_LIST_FILE = "data/categories.json"
PLAYER_LIST_FILE = "data/players.json"
TASK_LIST_FILE = "data/tasks.json"
INTERFACE_LIST_FILE = "data/interfaces.json"

def load_critical_config_file(path):
    """Load a file or print an error and quit."""
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        print(str(exc))
        print("Could not load/read {} D:".format(path))
        raise SystemExit

class TaskMistress(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.first_login = True

        self.config = load_critical_config_file(CONFIG_FILE)

        self.category_list = CategoryList(self, CATEGORY_LIST_FILE)
        self.player_list = PlayerList(self, PLAYER_LIST_FILE)
        self.task_list = TaskList(self, TASK_LIST_FILE)
        self.interface_list = InterfaceList(self, INTERFACE_LIST_FILE)

    def save_data(self):
        self.player_list.save()
        self.task_list.save()
        self.interface_list.save()

    def when_mentioned(self, message):
        return [
            '{} '.format(self.user.mention),
            '<@!{}> '.format(self.user.id)]

    async def on_command_error(self, ctx, error):
        log.exception(str(error), exc_info=error)
        await ctx.channel.send(str(error))

    async def on_ready(self):
        log.info("We have logged in as {}".format(self.user))
        self.first_login = False

    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bots
        await self.process_commands(message)

    async def on_raw_reaction_add(self, event):
        user = await bot.fetch_user(event.user_id)
        if user.bot:
            return  # Ignore bots
        if event.message_id in bot.interface_list:
            interface = bot.interface_list.get_value(event.message_id)
            log.info(f"Button '{event.emoji.name}' clicked on Interface {event.message_id}:")
            log.debug(repr(interface.handle_click))
            await interface.handle_click(event, user)


bot = TaskMistress(command_prefix=TaskMistress.when_mentioned)

@bot.group(hidden=True)
@commands.has_role("Administrator")
async def post(ctx):
    if ctx.invoked_subcommand is None:
        pass

@post.command()
async def actions(ctx):
    log.info(f"Executing `post actions` command for {ctx.author.display_name}.")
    channel = await bot.fetch_channel(bot.config['infoChannel'])
    await bot.interface_list.add_actions_interface(channel)
    await ctx.message.delete()

@post.command()
async def category_info(ctx):
    log.info(f"Executing `post category_info` command for {ctx.author.display_name}.")
    channel = await bot.fetch_channel(bot.config['infoChannel'])
    await bot.interface_list.add_category_info_interface(channel)
    await ctx.message.delete()

@bot.command()
async def assign(ctx, target: Member, task_id: typing.Optional[int]):
    """Give a task to a particular person."""
    raise NotImplementedError

@bot.command()
async def verify(ctx, task_id: int):
    """Verify the completion of a task."""
    raise NotImplementedError

@bot.group()
async def tasks(ctx):
    """Lists tasks you have created."""
    raise NotImplementedError

@tasks.command()
async def create(ctx):
    """Begin the process of creating a new task."""
    raise NotImplementedError

@tasks.command()
async def edit(ctx, task_id: int):
    """Edit a task you have created."""
    raise NotImplementedError

@tasks.command()
async def delete(ctx, task_id: int):
    """Mark a task as deleted."""
    raise NotImplementedError

@bot.group()
@commands.has_role("Operator")
async def categories(ctx):
    """No function."""
    if ctx.invoked_subcommand is None:
        pass

@categories.command()
async def add(ctx, name: str, emoji: Emoji, *, description):
    """Adds a new Category."""
    key, category = ctx.bot.category_list.add(ctx, name, emoji, description)
    await ctx.channel.send(f"New category {category.name}{category.emoji} added: {category.description}")

@categories.command()
async def remove(ctx, category_id: int):
    """Removes an existing category by ID."""
    raise NotImplementedError


def main():
    try:
        with open('token.txt', 'r') as file:
            bot.run(file.read())
    except IOError as exc:
        log.exception(exc, exc_info=exc)
        log.error("Could not load/read token.txt D:")
        raise SystemExit


if __name__ == "__main__":
    main()
