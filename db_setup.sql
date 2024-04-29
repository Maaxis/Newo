DROP TABLE IF EXISTS Tribes;
CREATE TABLE IF NOT EXISTS Tribes (
    snowflake VARCHAR(60) PRIMARY KEY,
    name TEXT NOT NULL,
    forum_id INTEGER DEFAULT NULL,
    discord_role_id BIGINT DEFAULT NULL,
    discord_channel_id BIGINT DEFAULT NULL
);

DROP TABLE IF EXISTS Confessionals;
CREATE TABLE IF NOT EXISTS Confessionals (
    snowflake VARCHAR(60) PRIMARY KEY,
    player VARCHAR(60),
    discord_channel_id BIGINT DEFAULT NULL,
    forum_id INTEGER DEFAULT NULL,
    submission_folder INTEGER DEFAULT NULL,
    voting_thread_id INTEGER DEFAULT NULL
);

DROP TABLE IF EXISTS Players;
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
    FOREIGN KEY (confessional) REFERENCES Confessionals(snowflake)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    FOREIGN KEY (tribe) REFERENCES Tribes(snowflake)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Alliances;
CREATE TABLE IF NOT EXISTS Alliances (
    snowflake VARCHAR(255) PRIMARY KEY,
    name TEXT,
    discord_channel_id BIGINT DEFAULT NULL,
    archived BOOLEAN DEFAULT FALSE
);

DROP TABLE IF EXISTS Allies;
CREATE TABLE IF NOT EXISTS Allies (
    player_id VARCHAR(60),
    alliance_id VARCHAR(255),
    PRIMARY KEY (player_id, alliance_id),
    FOREIGN KEY (player_id) REFERENCES Players(snowflake)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (alliance_id) REFERENCES Alliances(snowflake)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

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
     ('a-adventurous-softballs', 'adventurous-softballs', 1233588702941413477, FALSE),
     ('a-worthy-greases', 'worthy-greases', 1233588835724824638, FALSE);

INSERT INTO Allies (player_id, alliance_id) VALUES
     ('p-aziah', 'a-adventurous-softballs'),
     ('p-billy', 'a-adventurous-softballs'),
     ('p-kingston', 'a-adventurous-softballs'),
     ('p-kingston', 'a-worthy-greases'),
     ('p-lorelei', 'a-worthy-greases'),
     ('p-nichelle', 'a-worthy-greases');
