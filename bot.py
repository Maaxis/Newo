config_file = "default.ini"
beta_mode = False

from config import Permissions
import os
import discord
from discord import app_commands
from typing import Optional, Literal
from discord.utils import get
import database as db
import random
import time
import ndimtools as ndim
import logging
from datetime import datetime, timedelta
import asyncio

config = Permissions(os.path.join("Config", config_file))
category_tribes = discord.Object(id=config.get("category_tribes"))
category_confessionals = discord.Object(id=config.get("category_confessionals"))
category_alliances = discord.Object(id=config.get("category_alliances"))
server_id = config.get("server_id")
test_guild = discord.Object(id=server_id)
log_channel_id = config.get("log_channel_id")
bot_admin = 119117540818550786
#db_filename = os.path.join("Config", config.get("database"))
#db.set_db(db_filename)
#forum = ndim.Forum(subdomain=config.get("subdomain"))

async def log(message, bot):
    guild = bot.get_guild(server_id)
    if guild is None:
        try:
            guild = await bot.fetch_guild(server_id)
        except discord.NotFound:
            print(f"Guild with ID {server_id} not found.")
            return
        except discord.Forbidden:
            print(f"Bot does not have permission to access guild with ID {server_id}.")
            return
        except discord.HTTPException as e:
            print(f"Failed to fetch guild: {e}")
            return

    channel = guild.get_channel(log_channel_id)
    if channel is None:
        try:
            channel = await guild.fetch_channel(log_channel_id)
        except discord.NotFound:
            print(f"Channel with ID {log_channel_id} not found.")
            return
        except discord.Forbidden:
            print(f"Bot does not have permission to access channel with ID {log_channel_id}.")
            return
        except discord.HTTPException as e:
            print(f"Failed to fetch channel: {e}")
            return

    await channel.send(message)


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
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f'[{now}] [#{message.channel.name}] {message.author}: {message.content}')
        except AttributeError:
            print(f'[...] {message.author}: {message.content}')


bot = BotClient(_intents=discord.Intents(messages=True, guilds=True, members=True, message_content=True))

@bot.event
async def on_thread_create(thread):
    # Automatically lock the thread so that no one can be invited
    if thread.is_private:
        await thread.edit(invitable=False)
        host_role = config.get("host_role")
        viewer_role = config.get("viewer_role")
        await thread.send(content=f"<@&{host_role}> <@&{viewer_role}>")
        await log(f"New thread {thread.mention} has been automatically set to non-invitable.\nThe thread creator will also be unable to invite new members after 10 minutes.", bot)


@bot.event
async def on_thread_update(before, after):
    # Ensure that the thread remains locked for invites
    if after.is_private and after.invitable:
        await after.edit(invitable=False)
        print(f'Thread {after.name} has been locked again for new invites.')


@bot.event
async def on_thread_member_join(member):
    thread = member.thread
    created_at = thread.created_at
    now = datetime.now(tz=created_at.tzinfo)
    time_diff = now - created_at
    if time_diff >= timedelta(minutes=10):  # Adjust time as needed
        async for message in thread.history(limit=3):  # Adjust the limit if necessary
            if any(mention.id == member.id for mention in message.mentions):
                # Found the invite message
                author = message.author
                guild = thread.guild
                author_permissions = guild.get_member(author.id).guild_permissions
                if not author_permissions.manage_threads:
                    await thread.remove_user(member)
                    await thread.send(content="You should make a new alliance if you want to invite more people!")
                    invited_member = guild.get_member(member.id)
                    await log(
                            f"{thread.mention}: {author.mention} attempted to invite {invited_member.mention} to the thread and was blocked.",
                            bot)
                break  # Stop once the invite message is found


@bot.tree.command()
async def ping(interaction: discord.Interaction):
    """Test Newo's responsiveness."""
    await interaction.response.send_message("Pong!", ephemeral=True)

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
        player_roles = db.get_player_roles_as_dictionary()
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
                player_roles = db.get_player_roles_as_dictionary()
                role_id = player_roles[member]
                role = get(this_guild.roles, id=role_id)
                tribe_member_roles.append(role)
        for member in this_guild.members:  # for every user, if their player role is in tribe member roles, give them tribe role
            for role in member.roles:
                if role in tribe_member_roles:
                    player_snowflake = db.get_player_snowflake(discord_role_id=role.id)
                    if self.tribe_role not in member.roles: # ignore if tribe role already assigned
                        for p_role in member.roles:  # remove old tribe from roles
                            if p_role in all_tribe_roles:
                                await member.remove_roles(p_role)
                        await member.add_roles(self.tribe_role)  # add role
                    db.update_player_tribe(player_snowflake, self.tribe_id)
        self.disabled = True
        await interaction.delete_original_response()
        await interaction.followup.send(f"Tribe channel created! <#{self.tribe_channel.id}>")


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
        viewer_role = get(this_guild.roles, id=config.get("viewer_role"))
        host_role = get(this_guild.roles, id=config.get("host_role"))
        overwrites = {this_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                      host_role: discord.PermissionOverwrite(read_messages=True),
                      role: discord.PermissionOverwrite(read_messages=True),
                      viewer_role: discord.PermissionOverwrite(read_messages=True,
                                                               send_messages=False)}  # default permission cannot view channel
        channel = await this_guild.create_text_channel(name, overwrites=overwrites,
                                                       category=category_tribes)
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
                       status="Contestant, juror, or prejuror", placement="Placement, if eliminated",
                       forum_user_id="User ID on forum", confessional_forum="Forum ID for confessional",
                       submission_forum="Forum ID for submissions", voting_thread="Thread ID for voting")
async def player(interaction: discord.Interaction, name: str, role: discord.Role = None,
                 confessional_channel: discord.TextChannel = None,
                 tribe: discord.Role = None, status: Literal["Contestant", "Jury", "Prejury"] = None,
                 placement: int = None, forum_user_id: int = None, confessional_forum: int = None,
                 submission_forum: int = None, voting_thread: int = None):
    """Create a player."""
    this_guild = interaction.guild
    if tribe:
        tribe = db.get_tribe_snowflake(discord_role_id=tribe.id)
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
            # --- Make confessional channel --- #
            viewer_role = get(this_guild.roles, id=config.get("viewer_role"))
            host_role = get(this_guild.roles, id=config.get("host_role"))
            overwrites = {this_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                          host_role: discord.PermissionOverwrite(read_messages=True),
                          role: discord.PermissionOverwrite(read_messages=True),
                          viewer_role: discord.PermissionOverwrite(read_messages=config.get("Discord.Channel.Confessional.ViewersCanRead"),
                                                                   send_messages=config.get("Discord.Channel.Confessional.ViewersCanSpeak"))}
            # default permission cannot view channel TODO: test
            confessional_channel = await this_guild.create_text_channel(name, overwrites=overwrites,
                                                                        category=category_confessionals)
            print(f"Created text channel #{name}")
            confessional_channel = confessional_channel.id
            # -------------------------------- #
        confessional = db.add_confessional(player_snowflake=None, player_name=name,
                                           discord_channel_id=confessional_channel, forum_id=confessional_forum, voting_thread_id=voting_thread, submission_folder=submission_forum)  # Create confessional without player snowflake
        player = db.add_player(name=name, discord_role_id=role.id, forum_user_id=forum_user_id, confessional=confessional, tribe=tribe, contestant=contestant, jury=jury, prejury=prejury,
                               placement=placement)  # Create player
        db.update_confessional_with_player_snowflake(confessional, player)  # Update confessional with player snowflake
        subd = config.get("subdomain")
        res = (f"Player: {name}\nRole: {role.mention}\nChannel: <#{confessional_channel}>\nTribe: {tribe}\nBoard confessional: "
               f"<http://www.ndimforums.com/{subd}/forum.asp?forumid={confessional_forum}>\n"
               f"Submissions: <http://www.ndimforums.com/{subd}/forum.asp?forumid={submission_forum}>\n"
               f"Voting thread: <http://www.ndimforums.com/{subd}/thread.asp?threadid={voting_thread}>\n"
               f"Profile: http://www.ndimforums.com/{subd}/profile.asp?memberid={forum_user_id}\n"
               f"Contestant: {contestant}\nJury: {jury}\nPre-jury: {prejury}\nPlacement: {placement}\n"
               f"user ID: {snowflake}")
        await interaction.response.send_message(res)
    else:
        await interaction.response.send_message("Player already exists, no updates made")

@bot.tree.context_menu(name="Pin/Unpin Message")
async def pin_message(interaction: discord.Interaction, message: discord.Message):
    try:
        # Check if the message is already pinned
        if message.pinned:
            await message.unpin(reason=f"{interaction.user.name} used Unpin Message: {message.jump_url}")
            await interaction.response.send_message(f"Message unpinned by {interaction.user.name}: {message.jump_url}")
        else:
            await message.pin(reason=f"{interaction.user.name} used Pin Message: {message.jump_url}")
            await interaction.response.send_message(f"Message pinned by {interaction.user.name}: {message.jump_url}")
    except discord.Forbidden:
        await interaction.response.send_message("I don't have permission to pin/unpin messages.", ephemeral=True)
    except discord.HTTPException as e:
        await interaction.response.send_message(f"Failed to pin/unpin the message. Error: {e}", ephemeral=True)

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
    roll_results = [random.randint(1, limit) for r in range(rolls)]
    result = ', '.join(map(str, roll_results))
    res = f":game_die: Rolling **{rolls}d{limit}** for **{interaction.user.display_name}**... :game_die:\n# {result}"
    if rolls > 1:
        res = res + f"\nTotal: **{str(sum(roll_results))}**"
    await interaction.response.send_message(res)


#@bot.tree.command()
#` R  A  C  E  R `
#:green_square: :yellow_square: :green_square: :green_square: :yellow_square:"

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


async def start_selenium_tracker():
    #await ndim.track_activity(forum)
    pass


async def main():
    # Start the Discord bot and the Selenium tracker concurrently
    # Run the bot and Selenium in parallel
    await asyncio.gather(bot.start(get_token()), start_selenium_tracker())

if __name__ == '__main__':
    asyncio.run(main())
