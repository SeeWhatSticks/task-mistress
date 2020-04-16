import typing
from PlayerList import PlayerList
from TaskList import TaskList
from InterfaceList import InterfaceList
from discord import Member
from discord.ext import commands

class TaskMistress(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.SYMBOLS = {
            'CHECK_MARK': "\U00002705",
            'NUMBER_BUTTONS': {
                '1\U0000FE0F\U000020E3': 1,
                '1\U0000FE0F\U000020E3': 2,
                '3\U0000FE0F\U000020E3': 3,
                '4\U0000FE0F\U000020E3': 4,
                '5\U0000FE0F\U000020E3': 5
            },
            'BKWD_ARROW': "\U000025C0\U0000FE0F",
            'FRWD_ARROW': "\U000025B6\U0000FE0F",
            'AVAILABLE': "\U00002600\U0000FE0F",
            'UNAVAILABLE': "\U0001F319",
            'UNSET_ALL': "\U0001F3F4\U0000200D\U00002620\U0000FE0F",
            'SET_ALL': "\U0001F3F3\U0000FE0F",
            'BEG': "\U0001F3B0"
        }
        self.COLORS = {
            'default': 0x3300cc,
            'set': 0x003399,
            'verify': 0xff3399,
            'confirm': 0x33ff33,
            'error': 0xff3333
        }

        self.player_list = PlayerList(self)
        self.task_list = TaskList(self)
        self.interface_list = InterfaceList(self)

    async def check_prefix(self):
        return self.bot.user.mention

    async def on_ready(self):
        print("We have logged in as {}".format(self.user))

    async def on_message(self, message):
        if message.author.bot:
            return  # Ignore bots
        await self.process_commands(message)


bot = TaskMistress(command_prefix=TaskMistress.check_prefix)

@bot.command()
async def assign(ctx, target: Member, task_id: typing.Optional[int]):
    """Give a task to a particular person."""
    pass

@bot.command()
async def verify(ctx, task_id: int):
    """Verify the completion of a task."""
    pass

@bot.group()
async def tasks(ctx):
    """Lists tasks you have created."""
    pass

@tasks.command()
async def create(ctx):
    """Begin the process of creating a new task."""
    pass

@tasks.command()
async def edit(ctx, task_id: int):
    """Edit a task you have created."""
    pass

@tasks.command()
async def delete(ctx, task_id: int):
    """Mark a task as deleted."""
    pass

def main():
    # Get the Discord token from local a plaintext file
    with open('token.txt', 'r') as file:
        # This line causes the client to connect to Discord
        bot.run(file.read())


if __name__ == "__main__":
    main()
