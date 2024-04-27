import sqlite3 as sql

con = sql.connect("test.db")
cur = con.cursor()
def init_db():
    setup_file = open('db_setup.sql', 'r')
    setup_sql = setup_file.read()
    setup_file.close()
    cur.executescript(setup_sql)
    con.commit()
def add_player(name, discord_role_id=None, confessional=None, tribe=None, contestant=True, jury=False, prejury=False,
               placement=None):
    snowflake = "p-" + name  # temporary, switch to random generation
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
    name_s = "a-" + name.lower()
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
    return name_s

def add_tribe(name, forum_id=None, discord_role_id=None, discord_channel_id=None):
    name_s = "t-" + name.lower()
    cur.execute("""
        INSERT INTO Tribes (name, forum_id, discord_role_id, discord_channel_id)
        VALUES (?, ?, ?, ?)
        """, (name_s, forum_id, discord_role_id, discord_channel_id))
    con.commit()
    return name_s




# having both get_tribe_name_from_snowflake and get_player_name_from_snowflake
# is a bit redundant when they look nearly identical,
# but we're trying to avoid dynamically inferring the table to be used for security
def get_tribe_name_from_snowflake(snowflake):
    cur.execute("SELECT name FROM Tribes WHERE snowflake = ?", (str(snowflake),))
    name = cur.fetchone()
    if name:
        return name[0]
    else:
        return None

def get_player_name_from_snowflake(snowflake):
    cur.execute("SELECT name FROM Players WHERE snowflake = ?", (str(snowflake),))
    name = cur.fetchone()
    if name:
        return name[0]
    else:
        return None

def get_snowflake_from_discord_role(discord_role_id):
    cur.execute("SELECT snowflake FROM Players WHERE discord_role_id = ?", (str(discord_role_id),))
    snowflake = cur.fetchone()
    if snowflake:
        return snowflake[0]
    else:
        return None


def get_snowflakes_from_discord_roles(discord_roles):
    snowflakes = []
    for role in discord_roles:
        snowflakes.append(get_snowflake_from_discord_role(role))
    return snowflakes


def reset_alliance_tables():
    cur.executescript("""
    DROP TABLE Alliances;
    DROP TABLE Allies;
    """)
    init_db()





if __name__ == '__main__':
    init_db()
