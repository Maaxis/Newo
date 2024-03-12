import sqlite3 as sql
con = sql.connect("default1.db")
cur = con.cursor()

# Create the Tribes table
def init_db():
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Tribes (
        snowflake VARCHAR(60) PRIMARY KEY,
        name TEXT NOT NULL,
        players TEXT,
        forum_id INTEGER DEFAULT NULL,
        discord_tribe_role_id BIGINT DEFAULT NULL,
        discord_tribe_channel_id BIGINT DEFAULT NULL
    )
    ''')

    # Create the Confessionals table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Confessionals (
        snowflake VARCHAR(60) PRIMARY KEY,
        player VARCHAR(60),
        discord_confessional_channel_id BIGINT DEFAULT NULL,
        confessional_forum_id INTEGER DEFAULT NULL,
        submission_folder INTEGER DEFAULT NULL,
        voting_thread_id INTEGER DEFAULT NULL
    )
    ''')

    # Create the Players table
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Players (
        snowflake VARCHAR(60) PRIMARY KEY,
        name TEXT NOT NULL,
        discord_unique_role_id BIGINT DEFAULT NULL,
        confessional VARCHAR(60),
        tribe VARCHAR(60),
        contestant BOOLEAN DEFAULT TRUE,
        jury BOOLEAN DEFAULT FALSE,
        prejury BOOLEAN DEFAULT FALSE,
        placement INT DEFAULT NULL,
        FOREIGN KEY (confessional) REFERENCES Confessionals(snowflake),
        FOREIGN KEY (tribe) REFERENCES Tribes(snowflake)
    )
''')
    cur.execute('''
    CREATE TABLE IF NOT EXISTS Alliances (
        snowflake VARCHAR(255) PRIMARY KEY,
        name TEXT,
        players TEXT DEFAULT NULL,
        discord_alliance_channel_id BIGINT DEFAULT NULL,
        archived BOOLEAN DEFAULT FALSE)
''')

def insertexample():
    #cur.execute("CREATE TABLE players(snowflake, name, discord_unique_role_id, confessional, tribe)")
    #cur.execute("CREATE TABLE tribes(snowflake, name, players, forum_id)")
    #cur.execute("CREATE TABLE confessionals(snowflake, player, discord_channel_id, forum_id, forum_submission_folder, voting_thread_id)")
    cur.execute("""
        INSERT INTO players (snowflake, name, discord_unique_role_id, confessional, tribe) VALUES
            ('p-aziah', 'Aziah', 1201608872457142322, 'c-aziah', 't-voida'),
            ('p-oregano', 'Oregano', 1201608889976758393, 'c-oregano', 't-voida'),
            ('p-shrek', 'Shrek', 1201608896289190038, 'c-shrek', 't-voida'),
            ('p-lorelei', 'Lorelei', 1201608883093917726, 'c-lorelei', 't-voida'),
            ('p-billy', 'Billy', 1201608876542414848, 'c-billy', 't-cyclone'),
            ('p-prue', 'Prue', 1201608892933750815, 'c-prue', 't-cyclone'),
            ('p-kingston', 'Kingston', 1201608879721697322, 'c-kingston', 't-cyclone'),
            ('p-nichelle', 'Nichelle', 1201608886537425027, 'c-nichelle', 't-cyclone')
    """)
    cur.execute("""
        INSERT INTO tribes (snowflake, name, players, forum_id, discord_tribe_role_id, discord_tribe_channel_id) VALUES
            ('t-voida', 'Voida', 'p-aziah p-oregano p-shrek p-lorelei', 0, 1201608792102670447, 1201611858503794718),
            ('t-cyclone', 'Cyclone', 'p-billy p-prue p-kingston p-nichelle', 0, 1201608797513339000, 1201611814891421886)
    """)
    cur.execute("""
        INSERT INTO confessionals (snowflake, player, discord_confessional_channel_id, confessional_forum_id, submission_folder, voting_thread_id) VALUES
            ('c-aziah', 'p-aziah', 1201611930725515314, 0, 0, 0),
            ('c-oregano', 'p-oregano', 1201612381256691814, 0, 0, 0),
            ('c-shrek', 'p-shrek', 1201612479332110357, 0, 0, 0),
            ('c-lorelei', 'p-lorelei', 1201612159294115972, 0, 0, 0),
            ('c-billy', 'p-billy', 1201611981854093392, 0, 0, 0),
            ('c-prue', 'p-prue', 1201612430502010980, 0, 0, 0),
            ('c-kingston', 'p-kingston', 1201612029690122251, 0, 0, 0),
            ('c-nichelle', 'p-nichelle', 1201612215061581914, 0, 0, 0)
    """)
    con.commit()

def add_player(gameid, name, confessional = None, tribe = None):
    confessional_snowflake = confessional
    if not confessional:
        confessional_snowflake = "c-" + name.lower()
        add_confessional(gameid, name)


def add_confessional(gameid, player = None, forumid = None, forumsubmissionfolderid = None, votingthreadid = None):
    pass

def add_tribe(gameid, name, players = None):
    if not players:
        players = []
    pass




if __name__ == '__main__':
    init_db()
    insertexample()