import sqlite3 as sql
import string
import random

import os

db_filename = os.path.join("default.db")
con = sql.connect(db_filename)
cur = con.cursor()


def set_db(filename):
    #global con
    con = sql.connect(filename)
    #global cur
    cur = con.cursor()


debug = True

def rand_string(size=8, characters=string.ascii_lowercase + string.digits):
    return "-" + ''.join(random.choice(characters) for _ in range(size))


def init_db():
    setup_file = open('db_setup_exampleless.sql', 'r')
    setup_sql = setup_file.read()
    setup_file.close()
    cur.executescript(setup_sql)
    con.commit()
    print("Initialized database")
    return


def add_player(name, discord_role_id=None, confessional=None, tribe=None, contestant=True, jury=False, prejury=False,
               placement=None, forum_user_id=None):
    snowflake = "p-" + name.lower() + rand_string()
    if contestant:
        contestant = 1
    else:
        contestant = 0
    if jury:
        jury = 1
    else:
        jury = 0
    if prejury:
        prejury = 1
    else:
        prejury = 0
    cur.execute('''INSERT INTO Players (snowflake, name, discord_role_id, forum_user_id, confessional, tribe, contestant, jury, prejury, placement)
	VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (snowflake, name, discord_role_id, forum_user_id, confessional, tribe, contestant, jury, prejury, placement))
    con.commit()
    if debug:
        print("Committed INSERT INTO Players")
    return snowflake


def list_tribes():
    cur.execute('''
	SELECT snowflake, tribe FROM Players
	''')
    players = cur.fetchall()
    tribes_dict = {}
    for player in players:
        tribe = player[1]
        if tribe not in tribes_dict:
            tribes_dict[tribe] = []  # Create a new list if the tribe is not already in the dictionary
        tribes_dict[tribe].append(player[0])  # Append the player to the corresponding tribe list
    # Create the result list in the desired format
    result = [[tribe, members] for tribe, members in tribes_dict.items()]
    return result


# returns [[tribe1, [p1, p2, p3, ...], [tribe2, [p1, p2, p3, ...]...]]


def get_tribe_roles():
    cur.execute('''
	SELECT discord_role_id FROM Tribes
	''')
    rows = cur.fetchall()  # This will be a list of tuples
    return [row[0] for row in rows]  # Extract the first element from each tuple


def get_player_roles_as_dictionary():
    cur.execute('''
    SELECT name, discord_role_id FROM Players
    ''')
    rows = cur.fetchall()
    return {row[0]: row[1] for row in rows}



def add_alliance(name, players=None, discord_channel_id=None, archived=False):
    # players should be an array of snowflakes
    name_s = "a-" + name.lower() + rand_string()
    if archived:
        archived = 1
    else:
        archived = 0
    if not discord_channel_id:
        discord_channel_id = None
    # Inserting into Alliances table
    cur.execute("""
		INSERT INTO Alliances (snowflake, name, discord_channel_id, archived) 
		VALUES (?, ?, ?, ?)
		""",
                (name_s, name, discord_channel_id, archived))
    # Inserting into Allies table for each player
    if players:
        for player in players:
            cur.execute("""
				INSERT INTO Allies (player_id, alliance_id)
				VALUES (?, ?)
				""",
                        (player, name_s))
    con.commit()
    if debug:
        print("Committed INSERT INTO Alliances, INSERT INTO Allies")
    return name_s


def add_tribe(name, forum_id=None, discord_role_id=None, discord_channel_id=None):
    # Check if a tribe with the given discord_role_id already exists
    cur.execute("SELECT snowflake FROM Tribes WHERE discord_role_id = ?", (discord_role_id,))
    existing_tribe = cur.fetchone()

    if existing_tribe:
        if debug:
            print(f"Tribe with discord_role_id {discord_role_id} already exists. Returning existing snowflake.")
        return existing_tribe[0]
    name_s = "t-" + name.lower() + rand_string()
    cur.execute("""
		INSERT INTO Tribes (snowflake, name, forum_id, discord_role_id, discord_channel_id)
		VALUES (?, ?, ?, ?, ?)
		""", (name_s, name, forum_id, discord_role_id, discord_channel_id))
    con.commit()
    if debug:
        print(f"Committed INSERT INTO Tribes")
    return name_s


def update_player_tribe(player_snowflake, tribe_snowflake):
    cur.execute("UPDATE Players SET tribe = ? WHERE snowflake = ?",
                (str(tribe_snowflake), str(player_snowflake),))
    con.commit()
    if debug:
        print(f"Committed UPDATE Players SET tribe = {tribe_snowflake} WHERE snowflake = {player_snowflake}")
    return

def add_confessional(player_snowflake, player_name="", discord_channel_id=None, forum_id=None, submission_folder=None,
                     voting_thread_id=None):
    name_s = "c-" + player_name.lower() + rand_string()
    cur.execute("""
		INSERT INTO Confessionals (snowflake, player, discord_channel_id, forum_id, submission_folder, voting_thread_id)
		VALUES (?, ?, ?, ?, ?, ?)
		""", (name_s, player_snowflake, discord_channel_id, forum_id, submission_folder, voting_thread_id))
    con.commit()
    if debug:
        print(f"Committed INSERT INTO Confessionals")
    return name_s


# having both get_tribe_name_from_snowflake and get_player_name_from_snowflake
# is a bit redundant when they look nearly identical,
# but we're trying to avoid dynamically inferring the table for security
def get_tribe_name_from_snowflake(snowflake):
    cur.execute("SELECT name FROM Tribes WHERE snowflake = ?", (str(snowflake),))
    name = cur.fetchone()
    if name:
        return name[0]
    else:
        return None


def get_tribe_snowflake(name=None, discord_role_id=None):
    cur.execute("SELECT snowflake FROM Tribes WHERE name = ? OR discord_role_id = ?",
                (str(name), str(discord_role_id),))
    snowflake = cur.fetchone()
    if snowflake:
        return snowflake[0]
    else:
        return None


def get_player_name_from_snowflake(snowflake):
    cur.execute("SELECT name FROM Players WHERE snowflake = ?", (str(snowflake),))
    name = cur.fetchone()
    if name:
        return name[0]
    else:
        return None


def get_player_snowflake(name=None, discord_role_id=None):
    cur.execute("SELECT snowflake FROM Players WHERE name = ? OR discord_role_id = ?",
                (str(name), str(discord_role_id),))
    snowflake = cur.fetchone()
    if snowflake:
        return snowflake[0]
    else:
        return None


def get_snowflakes_from_player_roles(discord_roles):
    snowflakes = []
    for role in discord_roles:
        snowflakes.append(get_snowflake_from_player_role(role))
    return snowflakes


def update_confessional_with_player_snowflake(confessional_snowflake, player_snowflake):
    cur.execute("UPDATE Confessionals SET player = ? WHERE snowflake = ?",
                (str(player_snowflake), str(confessional_snowflake),))
    con.commit()
    if debug:
        print(f"Committed UPDATE Confessionals SET player = {player_snowflake} WHERE snowflake = {confessional_snowflake}")
    return




def quick_exec():
    pass


if __name__ == '__main__':
    quick_exec()
