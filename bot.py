import discord
from discord import app_commands
import logging
from typing import Optional, Literal
from discord.utils import get
import random_name
import database as db
import random

tribes_category = discord.Object(id=1201610069419237587)
confessionals_category = discord.Object(id=1201610161383547000)
alliances_category = discord.Object(id=1201610117267853322)


class Settings:
    def __init__(self, settings_file):
        pass


class Permissions:
    def __init__(self, config_file):
        self.config = self.load_config(config_file)

    def load_config(self, file_path):
        config = {}
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line and not line.startswith('#'):
                    key_path, value = line.split('=', 1)
                    value = value.strip()
                    keys = key_path.split('.')
                    current_dict = config
                    for key in keys[:-1]:
                        if key not in current_dict:
                            current_dict[key] = {}
                        current_dict = current_dict[key]
                    current_dict[keys[-1]] = value
        return config

    def convert_value(self, value):
        """Convert string values to appropriate data types."""
        if value.upper() == 'TRUE':
            return True
        elif value.upper() == 'FALSE':
            return False
        return value

    def get(self, path):
        """Retrieve a configuration value by specifying its path in dot notation."""
        keys = path.split('.')
        current_value = self.config
        for key in keys:
            current_value = current_value.get(key)
            if current_value is None:
                return None
        return self.convert_value(current_value)


config = Permissions("config.txt")

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
beta_mode = True


class AllianceCreator(discord.ui.Select):
    def __init__(self, alliance_name=None, user_id=None):
        self.alliance_name = alliance_name
        if self.alliance_name is None:
            self.alliance_name = random_name.gen_name()
        self.user_id = user_id
        options = []
        for key, val in player_roles.items():
            options.append(discord.SelectOption(label=key))
        options.append(
            discord.SelectOption(label="CANCEL", description="Cancel alliance creation", value="cancel"))
        _max = len(options)
        super().__init__(placeholder=f'Select alliance members.', min_values=1, max_values=_max,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You are not authorized to use this menu.", ephemeral=True)
            return
        await interaction.response.defer()
        if "cancel" in self.values:
            self.disabled = True
            await interaction.delete_original_response()
            await interaction.followup.send("Alliance creation canceled by user.")
            return
        alliance_members = self.values
        this_guild = interaction.guild
        alliance_member_roles = []
        viewer_role = get(this_guild.roles, id=1201610486572138636)
        host_role = get(this_guild.roles, id=1201608732983972022)
        for member in alliance_members:
            if member is not None:
                role_id = player_roles[member]
                role = get(this_guild.roles, id=role_id)
                alliance_member_roles.append(role)
        overwrites = {
            this_guild.default_role: discord.PermissionOverwrite(read_messages=False)
        }  # default permission cannot view channel
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
        if config.get("Discord.Channel.Alliance.ViewersCanRead"):
            overwrites[viewer_role] = discord.PermissionOverwrite(read_messages=True, send_messages=False)
        alliance_channel = await this_guild.create_text_channel(self.alliance_name, overwrites=overwrites,
                                                                category=alliances_category)
        print(f"Created text channel #{alliance_name}")
        intro_text = ""
        for role in alliance_member_roles:
            intro_text += (role.mention + " ")
        await alliance_channel.send(intro_text + f"created by {creator}.")
        print(alliance_member_roles)
        player_ids = db.get_snowflakes_from_player_roles(role_ids)
        print(player_ids)
        db.add_alliance(name=self.alliance_name, players=player_ids, discord_channel_id=alliance_channel.id,
                        archived=False)
        self.disabled = True
        await interaction.delete_original_response()
        await interaction.followup.send(f"Alliance channel created! <#{alliance_channel.id}>")


class TribeCreator(discord.ui.Select):
    def __init__(self, tribe_name=None, user_id=None, tribe_role=None, tribe_channel=None, tribe_id=None):
        self.tribe_name = tribe_name
        self.tribe_role = tribe_role
        self.tribe_channel = tribe_channel
        self.tribe_id = tribe_id
        if self.tribe_name is None:
            self.tribe_name = random_name.gen_name()
        self.user_id = user_id
        options = []
        for key, val in player_roles.items():  # switch this to non-test roles
            options.append(discord.SelectOption(label=key))
        options.append(
            discord.SelectOption(label="CANCEL", description="Cancel tribe member selection", value="cancel"))
        _max = len(options)
        super().__init__(placeholder=f'Select tribe members.', min_values=1, max_values=_max,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        this_guild = interaction.guild
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("You are not authorized to use this menu.", ephemeral=True)
            return
        await interaction.response.defer()
        if "cancel" in self.values:
            self.disabled = True
            await interaction.delete_original_response()
            await interaction.followup.send("Tribe member selection canceled by user.")
            return
        all_tribe_roles = []
        for tribe_role_id in db.get_tribe_roles():
            all_tribe_roles.append(get(this_guild.roles, id=tribe_role_id))
        tribe_members = self.values
        tribe_member_roles = []  # this will be a list of all tribe members, their player roles
        for member in tribe_members:
            if member is not None:
                role_id = player_roles[member]
                role = get(this_guild.roles, id=role_id)
                tribe_member_roles.append(role)
        for member in this_guild.members:  # for every user, if their player role is in tribe member roles, give them tribe role
            for role in member.roles:
                if role in tribe_member_roles:
                    player_snowflake = db.get_player_snowflake(discord_role_id=role.id)
                    for p_role in member.roles:  # remove old tribe from roles
                        if p_role in all_tribe_roles:
                            await member.remove_roles(p_role)
                    await member.add_roles(self.tribe_role)  # add role
                    db.update_player_tribe(player_snowflake, self.tribe_id)
        self.disabled = True
        await interaction.delete_original_response()
        await interaction.followup.send(f"Tribe channel created! <#{self.tribe_channel.id}>")


class AllianceCreatorInit(discord.ui.View):
    def __init__(self, alliance_name=None, user_id=None):
        super().__init__()
        alliance_name = alliance_name
        self.add_item(AllianceCreator(alliance_name=alliance_name, user_id=user_id))


class TribeCreatorInit(discord.ui.View):
    def __init__(self, tribe_name=None, user_id=None, tribe_role=None, tribe_channel=None, tribe_id=None):
        super().__init__()
        tribe_name = tribe_name
        tribe_role = tribe_role
        tribe_channel = tribe_channel
        tribe_id = tribe_id
        self.add_item(
            TribeCreator(tribe_name=tribe_name, user_id=user_id, tribe_role=tribe_role, tribe_channel=tribe_channel,
                         tribe_id=tribe_id))


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
        try:
            print(f'[#{message.channel.name}] {message.author}: {message.content}')
        except AttributeError:
            print(f'[...] {message.author}: {message.content}')


bot = BotClient(_intents=discord.Intents(messages=True, guilds=True, members=True, message_content=True))


@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Test Newo's responsiveness."""
    await interaction.response.send_message("Pong!", ephemeral=True)


@bot.tree.command()
@app_commands.describe(name="Name of the alliance. If left blank, will be randomized.")
async def alliance(interaction: discord.Interaction, name: Optional[str] = None):
    """Creates a private channel for an alliance."""
    view = AllianceCreatorInit(alliance_name=name, user_id=interaction.user.id)
    await interaction.response.send_message("Select alliance members. To cancel, select CANCEL.", view=view,
                                            ephemeral=True)


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
@app_commands.describe(name="Tribe name (required)", forum_id="Forum ID of tribe (last numbers in subforum URL)",
                       role="Tribe role. If left blank, we'll make one for you.",
                       channel="Tribe channel. If left blank, we'll make one for you.",
                       color="Tribe color, used for role creation. 6 character hexadecimal code. Leave blank to randomize.")
async def tribe(interaction: discord.Interaction, name: str, forum_id: int = None, role: discord.Role = None,
                channel: discord.TextChannel = None, color: str = None):
    """Create or edit a tribe."""
    this_guild = interaction.guild
    if color:
        color = discord.Color(int(color, 16))
    else:
        color = discord.Color(random.randint(0, 0xFFFFFF))
    if not role:
        role = await this_guild.create_role(name=name)
        print(f"Created role @{name}")
        roles = await this_guild.fetch_roles()
        await role.edit(position=len(roles) - 4, color=color, hoist=True)
    if not channel:
        viewer_role = get(this_guild.roles, id=1201610486572138636)
        host_role = get(this_guild.roles, id=1201608732983972022)
        overwrites = {this_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                      host_role: discord.PermissionOverwrite(read_messages=True),
                      role: discord.PermissionOverwrite(read_messages=True),
                      viewer_role: discord.PermissionOverwrite(read_messages=True,
                                                               send_messages=False)}  # default permission cannot view channel
        channel = await this_guild.create_text_channel(name, overwrites=overwrites,
                                                       category=tribes_category)
        print(f"Created channel #{name}")
    tribe_id = db.add_tribe(name, forum_id, discord_role_id=role.id, discord_channel_id=channel.id)
    view = TribeCreatorInit(tribe_name=name, user_id=interaction.user.id, tribe_role=role, tribe_channel=channel,
                            tribe_id=tribe_id)
    await interaction.response.send_message(
        "Select tribe members. If you don't need to edit tribe members, or you plan to assign roles manually, select CANCEL.",
        view=view, ephemeral=True)
    return tribe_id


@bot.tree.command()
@app_commands.describe(name="Player name (required)", role="Unique role for the individual player",
                       confessional_channel="Unique live confessional or production chat", tribe="Current tribe's role",
                       status="Contestant, juror, or prejuror", placement="Placement, if eliminated")
async def player(interaction: discord.Interaction, name: str, role: discord.Role = None,
                 confessional_channel: discord.TextChannel = None,
                 tribe: discord.Role = None, status: Literal["Contestant", "Jury", "Prejury"] = None,
                 placement: int = None):
    """Create a player."""
    this_guild = interaction.guild
    if tribe:
        tribe = db.get_tribe_snowflake(discord_role_id=tribe.id)
    print(tribe)
    contestant = 0
    jury = 0
    prejury = 0
    if status == "Contestant":
        contestant = 1
    elif status == "Jury":
        jury = 1
    elif status == "Prejury":
        prejury = 1
    # Check role ID, then name, to see if player exists
    snowflake = ""
    if role:
        snowflake = db.get_player_snowflake(discord_role_id=role.id)
    else:
        role = await this_guild.create_role(name=name)
        print(f"Created role @{name}")
    if not snowflake:
        snowflake = db.get_player_snowflake(name=name)
    print(snowflake)
    if not snowflake:  # If player does not exist
        if confessional_channel:
            confessional_channel = confessional_channel.id
        else:
            viewer_role = get(this_guild.roles, id=1201610486572138636)
            host_role = get(this_guild.roles, id=1201608732983972022)
            overwrites = {this_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                          host_role: discord.PermissionOverwrite(read_messages=True),
                          role: discord.PermissionOverwrite(read_messages=True),
                          viewer_role: discord.PermissionOverwrite(read_messages=True,
                                                                   send_messages=True)}  # default permission cannot view channel
            confessional_channel = await this_guild.create_text_channel(name, overwrites=overwrites,
                                                                        category=confessionals_category)
            print(f"Created text channel #{name}")
            confessional_channel = confessional_channel.id
        confessional = db.add_confessional(player_snowflake=None, player_name=name,
                                           discord_channel_id=confessional_channel)  # Create confessional without player snowflake
        player = db.add_player(name, role.id, confessional, tribe, contestant, jury, prejury,
                               placement)  # Create player
        db.update_confessional_with_player_snowflake(confessional, player)  # Update confessional with player snowflake
        player_roles[name] = role.id
        await interaction.response.send_message("Done")
    else:
        await interaction.response.send_message("Player already exists, no updates made")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


if __name__ == '__main__':
    bot.run(get_token(), log_level=logging.INFO)
