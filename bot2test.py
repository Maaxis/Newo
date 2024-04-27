import discord
from discord.ext import commands
from discord import app_commands
import logging
from typing import Optional, List, Literal
from discord.utils import get
import random_name
import database as db

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

test_guild = discord.Object(id=1201608522975150152)  # replace with your guild id
bot_admin = 119117540818550786
debug_mode = True
beta_mode = True

def get_role_from_id(guild, role_id):
    role = get(guild.roles, id=role_id)
    return role



def get_players_as_literal():
    return Literal["Aziah", "Billy", "Kingston", "Lorelei", "Nichelle", "Oregano", "Prue", "Shrek"]

def get_role_from_name_string():
    pass

def find_key_by_value(value):
    for key, val in player_roles.items():
        if val == value:
            return key
    return None

#alliance_category = get(guild.categories, id=1201610117267853322)

class AllianceCreator(discord.ui.Select):
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
        } # default permission cannot view channel
        creator = interaction.user.mention
        for role in interaction.user.roles:
            if role.id in player_roles.values():
                creator = role.mention
                if role not in alliance_member_roles:
                    alliance_member_roles.append(role)
                break
        role_ids = []
        overwrites[host_role] = discord.PermissionOverwrite(read_messages=True)
        for role in alliance_member_roles:
            overwrites[role] = discord.PermissionOverwrite(read_messages=True)
            role_ids.append(role.id)
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
        print(alliance_member_roles)
        player_ids = db.get_snowflakes_from_discord_roles(role_ids)
        print(player_ids)
        db.add_alliance(name=self.alliance_name, players=player_ids, discord_channel_id=alliance_channel.id, archived=False)
        await interaction.followup.send(f"Done! <#{alliance_channel.id}>")

class AllianceCreatorInit(discord.ui.View):
    def __init__(self, alliance_name=None):
        super().__init__()
        alliance_name = alliance_name
        self.add_item(AllianceCreator(alliance_name=alliance_name))

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

@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Test Newo's responsiveness."""
    await interaction.response.send_message("Pong!")

@bot.tree.command()
async def alliance(interaction: discord.Interaction, name: Optional[str] = None):
    """Creates a private channel for an alliance."""
    view = AllianceCreatorInit(alliance_name=name)
    await interaction.response.send_message("Select alliance members", view=view)

@bot.tree.command()
async def tribes(interaction: discord.Interaction):
    """Lists current tribes."""
    tribes = db.list_tribes()
    # returns [[tribe1, [p1, p2, p3, ...], [tribe2, [p1, p2, p3, ...]...]]
    msg = ""
    for tribe in tribes:
        tribe_snowflake = tribe[0]
        tribe_name = db.get_tribe_name_from_snowflake(tribe_snowflake)
        msg = msg + f"**{tribe_name}**: "
        players = tribe[1]
        for player in players:
            player_name = db.get_player_name_from_snowflake(player)
            msg = msg + f"{player_name} "
        msg = msg + "\n"
    await interaction.response.send_message(msg)


@bot.tree.command()
async def player(interaction: discord.Interaction, name: str, discord_role_id: int = None, confessional: str = None, tribe: str = None, contestant: bool = True, jury: bool = False, prejury: bool = False, placement: int = None):
    #if confessional == None:
    db.add_player(name, discord_role_id, confessional, tribe, contestant, jury, prejury, placement)
    await interaction.response.send_message("Done")




@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')



if __name__ == '__main__':
    bot.run(get_token(), log_level=logging.INFO)
