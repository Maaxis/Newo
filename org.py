import random
import string
from discord import Guild, Role, TextChannel
from typing import Literal


class Snowflake:
    # identifier for person, tribe, and confessional objects
    def __init__(self, prefix: str = None, snowflake: str = None):
        """
        Initializes a new instance of the class.

        Args:
            prefix (str, optional): The prefix to be used. Defaults to None.
            snowflake (str, optional): The snowflake to be used. Defaults to None.
        """
        self.snowflake = snowflake
        self.prefix = prefix
        if snowflake is None:
            self.generate_snowflake()

    def generate_snowflake(self):
        """
        Generate a snowflake.

        Args:
            self (obj): The current object instance.

        Returns:
            None
        """
        self.snowflake = self.prefix + ''.join(random.choices(string.ascii_letters + string.digits, k=20))


class Game(Snowflake):
    # abstract information about a game and its associated features
    def __init__(self, name: str, subdomain: str, players: list['Player'] = None, tribes: list['Tribe'] = None,
                 hosts: list['Person'] = None,
                 server: 'discord.Guild' = None, forum: 'Forum' = None):
        """
        Initializes a new instance of the class.
        Args:
            name (str): The name of the instance.
            subdomain (str): The subdomain of the instance.
            players (list['Player'], optional): The list of players. Defaults to None.
            tribes (list['Tribe'], optional): The list of tribes. Defaults to None.
            hosts (list['Person'], optional): The list of hosts. Defaults to None.
            server ('discord.Guild', optional): The Discord server object. Defaults to None.
            forum ('Forum', optional): The forum object. Defaults to None.
        """
        super().__init__(prefix="g-")
        self.name = name
        self.subdomain = subdomain
        self.players = players  # array of Players
        self.tribes = tribes  # array of Tribes
        self.hosts = hosts  # array of Persons
        self.server = server  # Discord Server object
        self.forum = forum  # Forum object
        if self.tribes is None:
            self.tribes = []
        if self.players is None:
            self.players = []
        if self.hosts is None:
            self.hosts = []


class Person(Snowflake):
    def __init__(self, game: Game = None, primary_group: str = None, discord_generic_role: discord.Role = None):
        """
        Initializes a new instance of the class.
        Args:
            game (Game, optional): The game object. Defaults to None.
            primary_group (str, optional): The primary group. Defaults to None.
            discord_generic_role (discord.Role, optional): The Discord generic role. Defaults to None.
        """
        super().__init__(prefix="p-")
        self.game = game
        self.primary_group = primary_group  # Viewer, Player, Host
        self.discord_generic_role = discord_generic_role  # discord role object


class Player(Person):
    def __init__(self, name: str = None, tribe: 'Tribe' = None, forum_user_id: int = None,
                 forum_confessional: int = None,
                 forum_submission_folder: int = None,
                 discord_personal_role: discord.Role = None, placement: int = 0, game: Game = None,
                 discord_generic_role: discord.Role = None,
                 subgroup: Literal['contender', 'jury', 'prejury', 'other'] = None):
        """
        Initializes a Player object.
        Args:
            name (str, optional): The name of the player. Defaults to None.
            tribe (Tribe, optional): The tribe the player belongs to. Defaults to None.
            forum_user_id (int, optional): The user ID of the player on the forum. Defaults to None.
            forum_confessional (int, optional): The confessional ID of the player on the forum. Defaults to None.
            forum_submission_folder (int, optional): The submission folder ID of the player on the forum. Defaults to None.
            discord_personal_role (discord.Role, optional): The personal Discord role of the player. Defaults to None.
            placement (int, optional): The placement of the player. Defaults to 0.
            game (Game, optional): The game the player is in. Defaults to None.
            discord_generic_role (discord.Role, optional): The generic Discord role of the player. Defaults to None.
            subgroup (Literal['contender', 'jury', 'prejury', 'other'], optional): The subgroup the player belongs to.
                Defaults to None.
        """
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
                                       forum_is_admin=False,
                                       forum_flood_control=0,
                                       forum_can_edit_own_posts=False,
                                       forum_can_remove_edited_by=False,
                                       forum_can_delete_own_posts=False,
                                       forum_can_edit_avatar=True,
                                       forum_can_edit_display_name=True,
                                       forum_can_use_rep_system=True,
                                       forum_can_use_pm_system=False,
                                       forum_show_group_on_active_user_lists=True,
                                       forum_can_see_viewer_forums=False,
                                       forum_can_see_general_forums=True,
                                       forum_can_see_all_tribe_forums=False,
                                       forum_can_see_all_confessionals=False,
                                       forum_can_see_jury_forum=False,
                                       forum_can_see_prejury_forum=False)
        self.name = name  # string player name
        self.tribe = self.set_tribe(tribe)  # tribe object, none if not alive
        self.forum_user_id = forum_user_id  # int
        self.forum_confessional = forum_confessional  # int
        self.forum_submission_folder = forum_submission_folder  # int
        self.discord_personal_role = discord_personal_role  # discord role object
        self.subgroup = subgroup  # Contender, Jury, Prejury
        self.placement = placement  # int, 0 if still in-game
        if self.subgroup == 'jury':
            self.set_juror(placement)
        if self.subgroup == 'prejury':
            self.set_prejuror(placement)

    def set_juror(self, placement: int):
        """
        Set the juror's placement and update the permissions.

        Args:
            placement (int): The placement of the juror.

        Returns:
            None
        """
        self.permissions.discord_can_see_jury_channel = True
        self.permissions.forum_can_see_jury_forum = True
        self.permissions.discord_display_role_members_separately = True
        self.placement = placement
        self.subgroup = "jury"

    def set_prejuror(self, placement: int):
        """
        Sets the prejuror for the given placement.

        Args:
            placement (int): The placement of the prejuror.

        Returns:
            None
        """
        self.permissions.discord_can_see_prejury_channel = True
        self.permissions.forum_can_see_prejury_forum = True
        self.permissions.discord_display_role_members_separately = True
        self.placement = placement
        self.subgroup = "prejury"

    def set_tribe(self, tribe):
        """
        Set the tribe of the player.

        Args:
            tribe (Tribe): The tribe to set for the player.

        Returns:
            Tribe: The tribe that the player is now a part of.
        """
        if tribe is not None and self not in tribe.players:
            tribe.players.append(self)
        return tribe


class Tribe(Snowflake):
    def __init__(self, name: str, game: Game = None, subdomain: str = None, players: list[Player] = None,
                 channel: discord.TextChannel = None, subforum: int = None):
        """
        Initializes a new instance of the class.

        Args:
            name (str): The name of the instance.
            game (Game, optional): The game associated with the instance. Defaults to None.
            subdomain (str, optional): The subdomain of the instance. Defaults to None.
            players (list[Player], optional): The list of players associated with the instance. Defaults to None.
            channel (discord.TextChannel, optional): The Discord channel associated with the instance. Defaults to None.
            subforum (int, optional): The ID of the subforum associated with the instance. Defaults to None.

        Returns:
            None

        """
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
        """
        Initializes an instance of the class.

        Args:
            subdomain (str): The subdomain of the instance.
            owner (Player, optional): The owner of the instance. Defaults to None.
            channel (discord.TextChannel, optional): The Discord channel of the instance. Defaults to None.
            subforum (int, optional): The ID of the subforum. Defaults to None.
            submission_folder (int, optional): The ID of the submission folder. Defaults to None.
            channel_viewer_readable (bool, optional): Whether the channel is viewer readable. Defaults to None.
            subforum_viewer_readable (bool, optional): Whether the subforum is viewer readable. Defaults to None.
        """
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
        """
        Initializes the object.

        Args:
            None

        Returns:
            None
        """
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
                                       forum_is_admin=False,
                                       forum_flood_control=0,
                                       forum_can_edit_own_posts=True,
                                       forum_can_remove_edited_by=True,
                                       forum_can_delete_own_posts=False,
                                       forum_can_edit_avatar=True,
                                       forum_can_edit_display_name=True,
                                       forum_can_use_rep_system=False,
                                       forum_can_use_pm_system=True,
                                       forum_show_group_on_active_user_lists=True,
                                       forum_can_see_viewer_forums=True,
                                       forum_can_see_general_forums=True,
                                       forum_can_see_all_tribe_forums=True,
                                       forum_can_see_all_confessionals=True,
                                       forum_can_see_jury_forum=True,
                                       forum_can_see_prejury_forum=True)


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
                 forum_is_admin=None,
                 forum_group=None,
                 forum_color=None,
                 forum_masks=None,
                 forum_flood_control=None,
                 forum_can_edit_own_posts=None,
                 forum_can_remove_edited_by=None,
                 forum_can_delete_own_posts=None,
                 forum_can_edit_avatar=None,
                 forum_can_edit_display_name=None,
                 forum_can_use_rep_system=None,
                 forum_can_use_pm_system=None,
                 forum_show_group_on_active_user_lists=None,
                 forum_can_see_viewer_forums=None,
                 forum_can_see_general_forums=None,
                 forum_can_see_all_tribe_forums=None,
                 forum_can_see_all_confessionals=None,
                 forum_can_see_jury_forum=None,
                 forum_can_see_prejury_forum=None):
        """
        Initializes a new instance of the class.

        Args:
            discord_is_admin (bool): Whether the user is an admin in the Discord server.
            discord_generic_role (str): The generic role of the user in the Discord server.
            discord_color (str): The color associated with the user in the Discord server.
            discord_display_role_members_separately (bool): Whether to display role members separately in the Discord server.
            discord_allow_anyone_to_mention (bool): Whether anyone can mention the user in the Discord server.
            discord_can_see_viewer_channels (bool): Whether the user can see viewer channels in the Discord server.
            discord_can_see_general_channels (bool): Whether the user can see general channels in the Discord server.
            discord_can_see_all_tribe_channels (bool): Whether the user can see all tribe channels in the Discord server.
            discord_can_see_all_alliance_channels (bool): Whether the user can see all alliance channels in the Discord server.
            discord_can_see_all_confessional_channels (bool): Whether the user can see all confessional channels in the Discord server.
            discord_can_see_jury_channel (bool): Whether the user can see the jury channel in the Discord server.
            discord_can_see_prejury_channel (bool): Whether the user can see the prejury channel in the Discord server.
            forum_is_admin (bool): Whether the user is an admin in the forum.
            forum_group (str): The group of the user in the forum.
            forum_color (str): The color associated with the user in the forum.
            forum_masks (list): The masks associated with the user in the forum.
            forum_flood_control (int): Whether flood control is enabled for the user in the forum.
            forum_can_edit_own_posts (bool): Whether the user can edit their own posts in the forum.
            forum_can_remove_edited_by (bool): Whether the user can remove the "edited by" tag in the forum.
            forum_can_delete_own_posts (bool): Whether the user can delete their own posts in the forum.
            forum_can_edit_avatar (bool): Whether the user can edit their avatar in the forum.
            forum_can_edit_display_name (bool): Whether the user can edit their display name in the forum.
            forum_can_use_rep_system (bool): Whether the user can use the reputation system in the forum.
            forum_can_use_pm_system (bool): Whether the user can use the private messaging system in the forum.
            forum_show_group_on_active_user_lists (bool): Whether to show the user's group on active user lists in the forum.
            forum_can_see_viewer_forums (bool): Whether the user can see viewer forums in the forum.
            forum_can_see_general_forums (bool): Whether the user can see general forums in the forum.
            forum_can_see_all_tribe_forums (bool): Whether the user can see all tribe forums in the forum.
            forum_can_see_all_confessionals (bool): Whether the user can see all confessionals in the forum.
            forum_can_see_jury_forum (bool): Whether the user can see the jury forum in the forum.
            forum_can_see_prejury_forum (bool): Whether the user can see the prejury forum in the forum.
        """
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
        self.forum_is_admin = forum_is_admin
        self.forum_group = forum_group
        self.forum_color = forum_color
        self.forum_masks = forum_masks
        self.forum_flood_control = forum_flood_control
        self.forum_can_edit_own_posts = forum_can_edit_own_posts
        self.forum_can_remove_edited_by = forum_can_remove_edited_by
        self.forum_can_delete_own_posts = forum_can_delete_own_posts
        self.forum_can_edit_avatar = forum_can_edit_avatar
        self.forum_can_edit_display_name = forum_can_edit_display_name
        self.forum_can_use_rep_system = forum_can_use_rep_system
        self.forum_can_use_pm_system = forum_can_use_pm_system
        self.forum_show_group_on_active_user_lists = forum_show_group_on_active_user_lists
        self.forum_can_see_viewer_forum = forum_can_see_viewer_forums
        self.forum_can_see_general_forums = forum_can_see_general_forums
        self.forum_can_see_all_tribe_forums = forum_can_see_all_tribe_forums
        self.forum_can_see_all_confessionals = forum_can_see_all_confessionals
        self.forum_can_see_jury_forum = forum_can_see_jury_forum
        self.forum_can_see_prejury_forum = forum_can_see_prejury_forum


def return_password(subdomain):
    """
    Return the password for the given subdomain.

    Args:
        subdomain (str): The subdomain for which the password is needed.

    Returns:
        str: The decoded password for the subdomain.
    """
    from secret import passwords
    import base64
    pw = base64.b64decode(passwords.get(subdomain))
    return pw.decode('utf-8')


def create_tribe(game: Game, name: str):
    """
    Create a new tribe and add it to the game.

    Args:
        game (Game): The game object.
        name (str): The name of the tribe.

    Returns:
        Tribe: The newly created tribe.
    """
    this_tribe = Tribe(name, game)
    game.tribes.append(this_tribe)
    return this_tribe


def create_tribes(game: Game, *names: str):
    """
    Create tribes based on the given names and add them to the game.

    Args:
        game (Game): The game object.
        *names (str): Variable-length argument list of tribe names.

    Returns:
        List[Tribe]: A list of created tribes.
    """
    tribes = []
    for name in names:
        tribe = create_tribe(game, name)
        tribes.append(tribe)
    return tribes


def create_player(game: Game, name: str):
    """
    Creates a new player object and adds it to the game.

    Args:
        game (Game): The game object to add the player to.
        name (str): The name of the player.

    Returns:
        Player: The newly created player object.
    """
    this_player = Player(name, game=game)
    if game.players is not None:
        game.players.append(this_player)
    return this_player


def create_players(game: Game, *names: str):
    """
    Create players for a game.

    Args:
        game (Game): The game object.
        *names (str): Variable number of player names.

    Returns:
        list: A list of created players.
    """
    cast = []
    for name in names:
        player = create_player(game, name)
        cast.append(player)
    return cast


def set_tribes_given_names(game: Game, **names):
    """
    Sets tribes for players based on their names.

    Args:
        game (Game): The game object containing the players and tribes.
        **names (dict): The names of the players and the corresponding tribe names.

    Returns:
        None
    """
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
                player_snowflake = obj.snowflake
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
