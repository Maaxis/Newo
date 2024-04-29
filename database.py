import sqlite3 as sql
import string
import random

con = sql.connect("test.db")
cur = con.cursor()


def rand_string(size=8, characters=string.ascii_lowercase + string.digits):
	return "-" + ''.join(random.choice(characters) for _ in range(size))


def init_db():
	setup_file = open('db_setup.sql', 'r')
	setup_sql = setup_file.read()
	setup_file.close()
	cur.executescript(setup_sql)
	con.commit()
	print("Initialized database")
	return


def add_player(name, discord_role_id=None, confessional=None, tribe=None, contestant=True, jury=False, prejury=False,
               placement=None):
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
	cur.execute('''INSERT INTO Players (snowflake, name, discord_role_id, confessional, tribe, contestant, jury, prejury, placement)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
	            (snowflake, name, discord_role_id, confessional, tribe, contestant, jury, prejury, placement))
	con.commit()
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
	print("Committed INSERT INTO Alliances, INSERT INTO Allies")
	return name_s


def add_tribe(name, forum_id=None, discord_role_id=None, discord_channel_id=None):
	name_s = "t-" + name.lower() + rand_string()
	cur.execute("""
        INSERT INTO Tribes (snowflake, name, forum_id, discord_role_id, discord_channel_id)
        VALUES (?, ?, ?, ?, ?)
        """, (name_s, name, forum_id, discord_role_id, discord_channel_id))
	con.commit()
	print(f"Committed INSERT INTO Tribes")
	return name_s


def add_confessional(player_snowflake, player_name="", discord_channel_id=None, forum_id=None, submission_folder=None, voting_thread_id=None):
	name_s = "c-" + player_name.lower() + rand_string()
	cur.execute("""
        INSERT INTO Confessionals (snowflake, player, discord_channel_id, forum_id, submission_folder, voting_thread_id)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (name_s, player_snowflake, discord_channel_id, forum_id, submission_folder, voting_thread_id))
	con.commit()
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


def get_snowflake_from_tribe_role(discord_role_id):
	cur.execute("SELECT snowflake FROM Tribes WHERE discord_role_id = ?", (str(discord_role_id),))
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


def get_snowflake_from_player_name(name):
	cur.execute("SELECT snowflake FROM Players WHERE name = ?", (str(name),))
	snowflake = cur.fetchone()
	if snowflake:
		return snowflake[0]
	else:
		return None


def get_snowflake_from_player_role(discord_role_id):
	cur.execute("SELECT snowflake FROM Players WHERE discord_role_id = ?", (str(discord_role_id),))
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
	cur.execute("UPDATE Confessionals SET player = ? WHERE snowflake = ?", (str(player_snowflake), str(confessional_snowflake),))
	con.commit()
	print(f"Committed UPDATE Confessionals SET player = {player_snowflake} WHERE snowflake = {confessional_snowflake}")
	return


def reset_alliance_tables():
	cur.executescript("""
    DROP TABLE Alliances;
    DROP TABLE Allies;
    """)
	init_db()


if __name__ == '__main__':
	init_db()
