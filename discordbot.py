# import org
from personality import personality
import ndimtools as ndim
# from ndimtools import User
import discord
# from discord.ext import commands
from discord import app_commands
# import chat_exporter
import urllib.request
import logging
import random
import typing

test_guild = discord.Object(id=1003884566232186880)  # replace with your guild id
bot_admin = 119117540818550786
debug_mode = True

filters = app_commands.Group(name="filters", description="...")
post = app_commands.Group(name="post", description="...")


class BotClient(discord.Client):
    def __init__(self, *, _intents: discord.Intents):
        super().__init__(intents=_intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=test_guild)
        await self.tree.sync(guild=test_guild)


intents = discord.Intents(messages=True, guilds=True, members=True)
bot = BotClient(_intents=intents)
forum = ndim.main()  # starts board driver





@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}.')
    print("------")
    global log_channel
    log_channel = bot.get_channel(1005565470553952287)
    await log_channel.send("Newo is connected.")


@bot.event
async def on_message(message: discord.Message):
    if message.author == bot.user:
        return
    if "newo" in message.content.lower():
        rng = random.randint(1, 100)
        print(rng)
        if rng == 1:
            msg = random.choice(personality)
            await message.channel.send(msg)


@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Test Newo's responsiveness."""
    await interaction.response.send_message("Pong!")


@bot.tree.command()
async def roll(interaction: discord.Interaction, dice: str):
    """Roll a die in NdN format.

    Parameters
    -----------
    dice: str
        XdY, where X = the number of dice and Y = the number of sides."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await interaction.response.send_message('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await interaction.response.send_message(result)


@bot.tree.command(description='Make a random choice.')
async def choose(interaction: discord.Interaction, choices: str, separator: str = ","):
    """Make a random choice. Use commas to separate choices.

    Parameters
    -----------
    choices: str
        The options, separate with commas by default.
    separator: str
        The delimiter separating the options.
    """
    await interaction.response.send_message(random.choice(choices.split(separator)))


@post.command(name="existingthread")
async def newpost(interaction: discord.Interaction, thread_id: int, content: str):
    """Have Newo post on a thread in this game's forum.

    Parameters
    -----------
    thread_id: int
        The thread ID to post to ("/threadasp?threadid=?")
    content: str
        The content of the post. You can also link a text file.
    """
    if debug_mode:
        debug = f"{interaction.user}: /post {str(thread_id)} {content}"
        await log_channel.send(debug)
        print(debug)
    if interaction.user.guild_permissions.administrator:  # require admin perms
        await interaction.response.send_message("Working on it...", ephemeral=True)
        try:  # TODO: catch exception for if thread doesn't exist
            ndim.navigate_thread(forum, str(thread_id))
            ndim.make_post(forum, content)
            await interaction.edit_original_response(content="Posted.")
        except Exception:
            await interaction.edit_original_response(content="Use /post [thread id] [content]")
    else:
        await interaction.response.send_message("You need to be a server administrator to use this command.")


@post.command(name="newthread")
async def newthread(interaction: discord.Interaction, forum_id: int, thread_title: str, post_content: str,
                    thread_description: str = "",
                    locked: bool = False,
                    pinned: bool = False,
                    poll: bool = False, poll_question: str = "", poll_options: str = None,
                    poll_num_of_options: int = 0,
                    poll_num_of_votes: int = 0):
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Working on it...")
        ndim.make_thread(forum, forum_id, thread_title, post_content, thread_description, locked, pinned, poll,
                         poll_question, poll_options, poll_num_of_options, poll_num_of_votes)
        await interaction.edit_original_response(content="Done")
    else:
        await interaction.response.send_message("You need to be a server administrator to use this command.")


@filters.command(name="import", description="test1")
async def _import(interaction: discord.Interaction,
                  url: str, separator: str = "|",
                  mode: typing.Literal['Full Word Only', 'Containing Word'] = 'Full Word Only'):
    """Import a list of word filters from a file.

    Parameters
    -----------
    url: str
        The URL with the raw text file.
    separator: str
        The delimiter used each line, default is |
    mode: typing.Literal['Full Word Only', 'Containing Word']
        The mode, default is Full Word Only
    """
    if debug_mode:
        debug = f"{interaction.user}: /import {url} {separator} {mode}"
        await log_channel.send(debug)
        print(debug)
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Working on it...")
        data = urllib.request.urlopen(url)
        ndim.login(forum, admin=True)
        ndim.navigate_edit_filters(forum.driver)
        for line in data:
            word_to_change = line.split(separator)[0].strip()
            _filter = line.split(separator)[1].strip()
            ndim.add_filter(word_to_change, _filter, mode, forum.driver)
        await interaction.edit_original_response(content="Done")
    else:
        await interaction.response.send_message("You need to be a server administrator to use this command.")


@filters.command(name="add")
async def add_one(interaction: discord.Interaction, filter: str, result: str,
                  mode: typing.Literal['Full Word Only', 'Containing Word'] = 'Full Word Only'):
    """Add one word filter.
    Parameters
    -----------
    filter: str
        The thing to be typed.
    result: str
        The resulting word the filter will be changed to.
    mode: typing.Literal['Full Word Only', 'Containing Word']
        The mode, default is Full Word Only.
    """
    if debug_mode:
        debug = f"{interaction.user}: /add {filter} {result} {mode}"
        await log_channel.send(debug)
        print(debug)
    if interaction.user.guild_permissions.administrator:
        await interaction.response.send_message("Working on it...")
        ndim.login(forum, admin=True)
        ndim.navigate_edit_filters(forum.driver)
        ndim.add_filter(filter, result, mode, forum.driver)
        await interaction.edit_original_response(content="Done")
    else:
        await interaction.response.send_message("You need to be a server administrator to use this command.")


def get_data(server: discord.Guild):  # lmao what is this for???
    pass


def get_token():
    from secret import token
    return token


bot.tree.add_command(filters)
bot.tree.add_command(post)
bot.run(get_token(), log_level=logging.INFO)
