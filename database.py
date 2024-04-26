import sqlite3 as sql

con = sql.connect("test.db")
cur = con.cursor()


def init_db():
    cur.executescript('''
CREATE TABLE IF NOT EXISTS Tribes (
    snowflake VARCHAR(60) PRIMARY KEY,
    name TEXT NOT NULL,
    forum_id INTEGER DEFAULT NULL,
    discord_role_id BIGINT DEFAULT NULL,
    discord_channel_id BIGINT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS Confessionals (
    snowflake VARCHAR(60) PRIMARY KEY,
    player VARCHAR(60),
    discord_channel_id BIGINT DEFAULT NULL,
    forum_id INTEGER DEFAULT NULL,
    submission_folder INTEGER DEFAULT NULL,
    voting_thread_id INTEGER DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS Players (
    snowflake VARCHAR(60) PRIMARY KEY,
    name TEXT NOT NULL,
    discord_role_id BIGINT DEFAULT NULL,
    confessional VARCHAR(60) DEFAULT NULL,
    tribe VARCHAR(60) DEFAULT NULL,
    contestant BOOLEAN DEFAULT TRUE,
    jury BOOLEAN DEFAULT FALSE,
    prejury BOOLEAN DEFAULT FALSE,
    placement INT DEFAULT NULL,
    FOREIGN KEY (confessional) REFERENCES Confessionals(snowflake),
    FOREIGN KEY (tribe) REFERENCES Tribes(snowflake)
);

CREATE TABLE IF NOT EXISTS Alliances (
    snowflake VARCHAR(255) PRIMARY KEY,
    name TEXT,
    discord_channel_id BIGINT DEFAULT NULL,
    archived BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS Allies (
    player_id VARCHAR(60),
    alliance_id VARCHAR(255),
    PRIMARY KEY (player_id, alliance_id),
    FOREIGN KEY (player_id) REFERENCES Players(snowflake),
    FOREIGN KEY (alliance_id) REFERENCES Alliances(snowflake)
);
''')


def insertexample():
    cur.executescript("""
INSERT INTO Tribes (snowflake, name, forum_id, discord_role_id, discord_channel_id) VALUES
    ('t-voida', 'Voida', NULL, 1201608792102670447, 1201611858503794718),
    ('t-cyclone', 'Cyclone', NULL, 1201608797513339000, 1201611814891421886);

INSERT INTO Confessionals (snowflake, player, discord_channel_id, forum_id, submission_folder, voting_thread_id) VALUES
    ('c-aziah', 'p-aziah', 1201611930725515314, NULL, NULL, NULL),
    ('c-oregano', 'p-oregano', 1201612381256691814, NULL, NULL, NULL),
    ('c-shrek', 'p-shrek', 1201612479332110357, NULL, NULL, NULL),
    ('c-lorelei', 'p-lorelei', 1201612159294115972, NULL, NULL, NULL),
    ('c-billy', 'p-billy', 1201611981854093392, NULL, NULL, NULL),
    ('c-prue', 'p-prue', 1201612430502010980, NULL, NULL, NULL),
    ('c-kingston', 'p-kingston', 1201612029690122251, NULL, NULL, NULL),
    ('c-nichelle', 'p-nichelle', 1201612215061581914, NULL, NULL, NULL);

INSERT INTO Players (snowflake, name, discord_role_id, confessional, tribe) VALUES
    ('p-aziah', 'Aziah', 1201608872457142322, 'c-aziah', 't-voida'),
    ('p-oregano', 'Oregano', 1201608889976758393, 'c-oregano', 't-voida'),
    ('p-shrek', 'Shrek', 1201608896289190038, 'c-shrek', 't-voida'),
    ('p-lorelei', 'Lorelei', 1201608883093917726, 'c-lorelei', 't-voida'),
    ('p-billy', 'Billy', 1201608876542414848, 'c-billy', 't-cyclone'),
    ('p-prue', 'Prue', 1201608892933750815, 'c-prue', 't-cyclone'),
    ('p-kingston', 'Kingston', 1201608879721697322, 'c-kingston', 't-cyclone'),
    ('p-nichelle', 'Nichelle', 1201608886537425027, 'c-nichelle', 't-cyclone');

INSERT INTO Alliances (snowflake, name, discord_channel_id, archived) VALUES
     ('a-busy-foods', 'busy-foods', 1201611930725515314, FALSE),
     ('a-well-informed-pastries', 'well-informed-pastries', 1210606264288022568, FALSE);

INSERT INTO Allies (player_id, alliance_id) VALUES
     ('p-aziah', 'a-busy-foods'),
     ('p-oregano', 'a-busy-foods'),
     ('p-prue', 'a-busy-foods'),
     ('p-kingston', 'a-well-informed-pastries'),
     ('p-lorelei', 'a-well-informed-pastries'),
     ('p-prue', 'a-well-informed-pastries');     
    """)
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
    tribes = []
    result = []
    for player in players:
        if player[1] not in tribes:
            tribes.append(player[1])  # get list of unique tribes
    for tribe in tribes:
        tribe_list = [tribe]
        player_list = []
        for player in players:  # this is inefficient?
            if player[1] == tribe:
                player_list.append(player[0])
        tribe_list.append(player_list)
        result.append(tribe_list)
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


# redundancy!!!
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


def get_array_of_snowflakes_from_array_of_discord_roles(discord_roles):
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
