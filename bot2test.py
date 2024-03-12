# import org
# from personality import personality
# from ndimtools import User
import discord
# from discord.ext import commands
from discord import app_commands
# import chat_exporter
# import urllib.request
import logging
# import random
# import typing
from typing import Optional, List, Literal
import database
from discord.utils import get
import random_name

import discord
from discord.ext import commands






player_roles = {
    'Aziah': 1201608872457142322,
    'Billy': 1201608876542414848,
    'Kingston': 1201608879721697322,
    'Lorelei': 1201608883093917726,
    'Nichelle': 1201608886537425027,
    'Oregano': 1201608889976758393,
    'Prue': 1201608892933750815,
    'Shrek': 1201608896289190038
}

def player_roles_setup():
    pass

test_guild = discord.Object(id=1201608522975150152)  # replace with your guild id
bot_admin = 119117540818550786
debug_mode = True
beta_mode = True

player_roles_setup()

def get_role_from_id(guild, role_id):
    role = get(guild.roles, id=role_id)
    return role

#alliance_category = get(guild.categories, id=1201610117267853322)

class Alliance_Dropdown(discord.ui.Select):
    def __init__(self, alliance_name=None):
        self.alliance_name = alliance_name
        options = []
        for key, val in player_roles.items():
            options.append(discord.SelectOption(label=key))
        max = len(options)
        super().__init__(placeholder='Select members of the alliance chat', min_values=1, max_values=max, options=options)

    async def callback(self, interaction: discord.Interaction):
        alliance_members = self.values
        this_guild = interaction.guild
        alliance_member_roles = []
        viewer_role = get_role_from_id(this_guild, 1201610486572138636)
        host_role = get_role_from_id(this_guild, 1201608732983972022)
        for member in alliance_members:
            if member is not None:
                role_id = player_roles[member]
                role = get_role_from_id(this_guild, role_id)
                alliance_member_roles.append(role)
        overwrites = {
            this_guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }
        creator = interaction.user.mention
        for role in interaction.user.roles:
            if role.id in player_roles.values():
                creator = role.mention
                if role not in alliance_member_roles:
                    alliance_member_roles.append(role)
                break
        overwrites[host_role] = discord.PermissionOverwrite(read_messages=True)
        for role in alliance_member_roles:
            overwrites[role] = discord.PermissionOverwrite(read_messages=True)
        ViewersCanReadAlliances = True
        if ViewersCanReadAlliances:
            overwrites[viewer_role] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
        if self.alliance_name is None:
            self.alliance_name = random_name.gen_name()
        alliance_channel = await this_guild.create_text_channel(self.alliance_name, overwrites=overwrites)
        intro_text = ""
        for role in alliance_member_roles:
            intro_text += (role.mention + " ")
        await alliance_channel.send(intro_text + f"created by {creator}.")
        await interaction.followup.send(f"Done! <#{alliance_channel.id}>")

class DropdownView(discord.ui.View):
    def __init__(self, alliance_name=None):
        super().__init__()
        alliance_name = alliance_name
        self.add_item(Alliance_Dropdown(alliance_name=alliance_name))



def get_token():
    t = ""
    if beta_mode:
        from secret import token_beta
        t = token_beta
    else:
        from secret import token
        t = token
    return t

class BotClient(discord.Client):
    def __init__(self, *, _intents: discord.Intents):
        super().__init__(intents=_intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        self.tree.copy_global_to(guild=test_guild)
        await self.tree.sync(guild=test_guild)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents(messages=True, guilds=True, members=True)
bot = BotClient(_intents=intents)


def get_players_as_literal():
    return Literal["Aziah", "Billy", "Kingston", "Lorelei", "Nichelle", "Oregano", "Prue", "Shrek"]

def get_role_from_name_string():
    pass

def find_key_by_value(value):
    for key, val in player_roles.items():
        if val == value:
            return key
    return None

@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Test Newo's responsiveness."""
    await interaction.response.send_message("Pong!")

@bot.tree.command()
async def alliance(interaction: discord.Interaction, name: Optional[str] = None):
    view = DropdownView(alliance_name=name)
    await interaction.response.send_message("Select alliance members", view=view)






@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


@bot.tree.command()
async def hello(interaction: discord.Interaction):
    """Says hello!"""
    await interaction.response.send_message(f'Hi, {interaction.user.mention}')


@bot.tree.command()
@app_commands.describe(
    first_value='The first value you want to add something to',
    second_value='The value you want to add to the first value',
)
async def add(interaction: discord.Interaction, first_value: int, second_value: int):
    """Adds two numbers together."""
    await interaction.response.send_message(f'{first_value} + {second_value} = {first_value + second_value}')


# The rename decorator allows us to change the display of the parameter on Discord.
# In this example, even though we use `text_to_send` in the code, the client will use `text` instead.
# Note that other decorators will still refer to it as `text_to_send` in the code.
@bot.tree.command()
@app_commands.rename(text_to_send='text')
@app_commands.describe(text_to_send='Text to send in the current channel')
async def send(interaction: discord.Interaction, text_to_send: str):
    """Sends the text into the current channel."""
    await interaction.response.send_message(text_to_send)


# To make an argument optional, you can either give it a supported default argument
# or you can mark it as Optional from the typing standard library. This example does both.
@bot.tree.command()
@app_commands.describe(member='The member you want to get the joined date from; defaults to the user who uses the command')
async def joined(interaction: discord.Interaction, member: Optional[discord.Member] = None):
    """Says when a member joined."""
    # If no member is explicitly provided then we use the command user here
    member = member or interaction.user

    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined {discord.utils.format_dt(member.joined_at)}')


# A Context Menu command is an app command that can be run on a member or on a message by
# accessing a menu within the client, usually via right clicking.
# It always takes an interaction as its first parameter and a Member or Message as its second parameter.

# This context menu command only works on members
@bot.tree.context_menu(name='Show Join Date')
async def show_join_date(interaction: discord.Interaction, member: discord.Member):
    # The format_dt function formats the date time into a human readable representation in the official client
    await interaction.response.send_message(f'{member} joined at {discord.utils.format_dt(member.joined_at)}')



if __name__ == '__main__':
    bot.run(get_token(), log_level=logging.INFO)