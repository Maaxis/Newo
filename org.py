import random
import string
import discord
from typing import Literal


class Snowflake:
    # identifier for person, tribe, and confessional objects
    def __init__(self, prefix: str = None, snowflake: str = None):
        self.snowflake = snowflake
        self.prefix = prefix
        if snowflake is None:
            self.generate_snowflake()

    def generate_snowflake(self):
        self.snowflake = self.prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=20))


class Game(Snowflake):
    # abstract information about a game and its associated features
    def __init__(self, name: str, subdomain: str, players: list['Player'] = None, tribes: list['Tribe'] = None,
                 hosts: list['Person'] = None,
                 server: 'discord.Guild' = None, board: 'Board' = None):
        super().__init__(prefix="g-")
        self.name = name
        self.subdomain = subdomain
        self.players = players  # array of Players
        self.tribes = tribes  # array of Tribes
        self.hosts = hosts  # array of Persons
        self.server = server  # Discord Server object
        self.board = board  # Board object
        if self.tribes is None:
            self.tribes = []
        if self.players is None:
            self.players = []
        if self.hosts is None:
            self.hosts = []


class Person(Snowflake):
    def __init__(self, game: Game = None, primary_group: str = None, discord_generic_role: discord.Role = None):
        super().__init__(prefix="p-")
        self.game = game
        self.primary_group = primary_group  # Viewer, Player, Host
        self.discord_generic_role = discord_generic_role  # discord role object


class Player(Person):
    def __init__(self, name: str = None, tribe: 'Tribe' = None, board_user_id: int = None,
                 board_confessional: int = None,
                 board_submission_folder: int = None,
                 discord_personal_role: discord.Role = None, placement: int = 0, game: Game = None,
                 discord_generic_role: discord.Role = None,
                 subgroup: Literal['contender', 'jury', 'prejury', 'other'] = None):
        super().__init__(game=game, primary_group="Player", discord_generic_role=discord_generic_role)
        self.permissions = Permissions(discord_is_admin=False,
                                       discord_display_role_members_separately=False,
                                       discord_allow_anyone_to_mention=False,
                                       discord_can_see_viewer_channels=False,
                                       discord_can_see_general_channels=True,
                                       discord_can_see_all_tribe_channels=False,
                                       discord_can_see_all_alliance_channels=False,
                                       discord_can_see_all_confessional_channels=False,
                                       discord_can_see_jury_channel=False,
                                       discord_can_see_prejury_channel=False,
                                       board_is_admin=False,
                                       board_flood_control=0,
                                       board_can_edit_own_posts=False,
                                       board_can_remove_edited_by=False,
                                       board_can_delete_own_posts=False,
                                       board_can_edit_avatar=True,
                                       board_can_edit_display_name=True,
                                       board_can_use_rep_system=True,
                                       board_can_use_pm_system=False,
                                       board_show_group_on_active_user_lists=True,
                                       board_can_see_viewer_forums=False,
                                       board_can_see_general_forums=True,
                                       board_can_see_all_tribe_forums=False,
                                       board_can_see_all_confessionals=False,
                                       board_can_see_jury_forum=False,
                                       board_can_see_prejury_forum=False)
        self.name = name  # string player name
        self.tribe = self.set_tribe(tribe)  # tribe object, none if not alive
        self.board_user_id = board_user_id  # int
        self.board_confessional = board_confessional  # int
        self.board_submission_folder = board_submission_folder  # int
        self.discord_personal_role = discord_personal_role  # discord role object
        self.subgroup = subgroup  # Contender, Jury, Prejury
        self.placement = placement  # int, 0 if still in-game
        if self.subgroup == 'jury':
            self.set_juror(placement)
        if self.subgroup == 'prejury':
            self.set_prejuror(placement)

    def set_juror(self, placement):
        self.permissions.discord_can_see_jury_channel = True
        self.permissions.board_can_see_jury_forum = True
        self.permissions.discord_display_role_members_separately = True
        self.placement = placement
        self.subgroup = "jury"

    def set_prejuror(self, placement):
        self.permissions.discord_can_see_prejury_channel = True
        self.permissions.board_can_see_prejury_forum = True
        self.permissions.discord_display_role_members_separately = True
        self.placement = placement
        self.subgroup = "prejury"

    def set_tribe(self, tribe):
        if tribe is not None and self not in tribe.players:
            tribe.players.append(self)
        return tribe


class Tribe(Snowflake):
    def __init__(self, name: str, game: Game = None, subdomain: str = None, players: list[Player] = None,
                 channel: discord.TextChannel = None, subforum: int = None):
        super().__init__(prefix="t-")
        self.name = name
        self.game = game
        self.subdomain = subdomain  # subdomain
        self.players = players  # array of Players
        self.channel = channel  # Discord channel
        self.subforum = subforum  # int id
        if self.players is None:
            self.players = []


class Confessional(Snowflake):
    def __init__(self, subdomain: str, owner: Player = None, channel: discord.TextChannel = None,
                 subforum: int = None, submission_folder: int = None, channel_viewer_readable: bool = None,
                 subforum_viewer_readable: bool = None):
        super().__init__(prefix="c-")
        self.subdomain = subdomain
        self.owner = owner  # player
        self.channel = channel  # Discord channel
        self.subforum = subforum  # int id
        self.submission_folder = submission_folder  # int id
        self.channel_viewer_readable = channel_viewer_readable  # True, False, or None to inherit global perms
        self.subforum_viewer_readable = subforum_viewer_readable  # True, False, or None to inherit global perms


class Viewer(Person):
    def __init__(self):
        super().__init__()
        self.permissions = Permissions(discord_is_admin=False,
                                       discord_display_role_members_separately=True,
                                       discord_allow_anyone_to_mention=False,
                                       discord_can_see_viewer_channels=True,
                                       discord_can_see_general_channels=True,
                                       discord_can_see_all_tribe_channels=True,
                                       discord_can_see_all_alliance_channels=True,
                                       discord_can_see_all_confessional_channels=True,
                                       discord_can_see_jury_channel=True,
                                       discord_can_see_prejury_channel=True,
                                       board_is_admin=False,
                                       board_flood_control=0,
                                       board_can_edit_own_posts=True,
                                       board_can_remove_edited_by=True,
                                       board_can_delete_own_posts=False,
                                       board_can_edit_avatar=True,
                                       board_can_edit_display_name=True,
                                       board_can_use_rep_system=False,
                                       board_can_use_pm_system=True,
                                       board_show_group_on_active_user_lists=True,
                                       board_can_see_viewer_forums=True,
                                       board_can_see_general_forums=True,
                                       board_can_see_all_tribe_forums=True,
                                       board_can_see_all_confessionals=True,
                                       board_can_see_jury_forum=True,
                                       board_can_see_prejury_forum=True)


class Permissions:
    def __init__(self,
                 discord_is_admin=None,
                 discord_generic_role=None,
                 discord_color=None,
                 discord_display_role_members_separately=None,
                 discord_allow_anyone_to_mention=None,
                 discord_can_see_viewer_channels=None,
                 discord_can_see_general_channels=None,
                 discord_can_see_all_tribe_channels=None,
                 discord_can_see_all_alliance_channels=None,
                 discord_can_see_all_confessional_channels=None,
                 discord_can_see_jury_channel=None,
                 discord_can_see_prejury_channel=None,
                 board_is_admin=None,
                 board_group=None,
                 board_color=None,
                 board_masks=None,
                 board_flood_control=None,
                 board_can_edit_own_posts=None,
                 board_can_remove_edited_by=None,
                 board_can_delete_own_posts=None,
                 board_can_edit_avatar=None,
                 board_can_edit_display_name=None,
                 board_can_use_rep_system=None,
                 board_can_use_pm_system=None,
                 board_show_group_on_active_user_lists=None,
                 board_can_see_viewer_forums=None,
                 board_can_see_general_forums=None,
                 board_can_see_all_tribe_forums=None,
                 board_can_see_all_confessionals=None,
                 board_can_see_jury_forum=None,
                 board_can_see_prejury_forum=None):
        self.discord_is_admin = discord_is_admin
        self.discord_generic_role = discord_generic_role
        self.discord_color = discord_color
        self.discord_display_role_members_separately = discord_display_role_members_separately
        self.discord_allow_anyone_to_mention = discord_allow_anyone_to_mention
        self.discord_can_see_viewer_channels = discord_can_see_viewer_channels
        self.discord_can_see_general_channels = discord_can_see_general_channels
        self.discord_can_see_all_tribe_channels = discord_can_see_all_tribe_channels
        self.discord_can_see_all_alliance_channels = discord_can_see_all_alliance_channels
        self.discord_can_see_all_confessional_channels = discord_can_see_all_confessional_channels
        self.discord_can_see_jury_channel = discord_can_see_jury_channel
        self.discord_can_see_prejury_channel = discord_can_see_prejury_channel
        self.board_is_admin = board_is_admin
        self.board_group = board_group
        self.board_color = board_color
        self.board_masks = board_masks
        self.board_flood_control = board_flood_control
        self.board_can_edit_own_posts = board_can_edit_own_posts
        self.board_can_remove_edited_by = board_can_remove_edited_by
        self.board_can_delete_own_posts = board_can_delete_own_posts
        self.board_can_edit_avatar = board_can_edit_avatar
        self.board_can_edit_display_name = board_can_edit_display_name
        self.board_can_use_rep_system = board_can_use_rep_system
        self.board_can_use_pm_system = board_can_use_pm_system
        self.board_show_group_on_active_user_lists = board_show_group_on_active_user_lists
        self.board_can_see_viewer_forum = board_can_see_viewer_forums
        self.board_can_see_general_forums = board_can_see_general_forums
        self.board_can_see_all_tribe_forums = board_can_see_all_tribe_forums
        self.board_can_see_all_confessionals = board_can_see_all_confessionals
        self.board_can_see_jury_forum = board_can_see_jury_forum
        self.board_can_see_prejury_forum = board_can_see_prejury_forum


def return_password(subdomain):
    from secret import passwords
    import base64
    pw = base64.b64decode(passwords.get(subdomain))
    return pw.decode('utf-8')


def create_tribe(game: Game, name: str):
    this_tribe = Tribe(name, game)
    game.tribes.append(this_tribe)
    return this_tribe


def create_tribes(game: Game, *names: str):
    tribes = []
    for name in names:
        tribe = create_tribe(game, name)
        tribes.append(tribe)
    return tribes


def create_player(game: Game, name: str):
    this_player = Player(name, game=game)
    if game.players is not None:
        game.players.append(this_player)
    return this_player


def create_players(game: Game, *names: str):
    cast = []
    for name in names:
        player = create_player(game, name)
        cast.append(player)
    return cast


def set_tribes_given_names(game: Game, **names):
    for player_name, tribe_name in names.items():
        for player_obj in game.players: # identify player by name
            if player_obj.name == player_name:
                this_player = player_obj
                for tribe_obj in game.tribes:
                    if tribe_obj.name == tribe_name:
                        this_player.set_tribe(tribe_obj)
                        break


def test(game, *database, **names):
    for name, tribe in names:
        for obj in database:
            if obj.game == game and obj.name == name and obj.subgroup == 'contender':
                player_snowflake = obj.snowflakef
            #if obj.game == game and obj.name == tribe and obj.

def set_tribes_given_snowflakes(game: Game, **snowflakes):
    pass


def return_object_via_snowflake(snowflake, *database): # just test func rn, pass in list of objects
    for obj in database:
        if obj.snowflake == snowflake:
            return obj


if __name__ == '__main__':
    # main()
    pass
