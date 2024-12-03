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
    forum_user_id INT DEFAULT NULL,
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

INSERT INTO Tribes (snowflake, name, forum_id, discord_role_id, discord_channel_id) VALUES
    ('t-voida-abcdefgh', 'Voida', 6, 1201608792102670447, 1201611858503794718),
    ('t-cyclone-abcdefgh', 'Cyclone', 7, 1201608797513339000, 1201611814891421886);
    
INSERT INTO Confessionals (snowflake, player, discord_channel_id, forum_id, submission_folder, voting_thread_id) VALUES
    ('c-aziah-abcdefgh', 'p-aziah-abcdefgh', 1201611930725515314, 8, 16, 6),
    ('c-billy-abcdefgh', 'p-billy-abcdefgh', 1201611981854093392, 9, 17, 7),
    ('c-kingston-abcdefgh', 'p-kingston-abcdefgh', 1201612029690122251, 10, 18, 8),
    ('c-lorelei-abcdefgh', 'p-lorelei-abcdefgh', 1201612159294115972, 11, 19, 9),
    ('c-nichelle-abcdefgh', 'p-nichelle-abcdefgh', 1201612215061581914, 12, 20, 10),
    ('c-oregano-abcdefgh', 'p-oregano-abcdefgh', 1201612381256691814, 13, 21, 11),
    ('c-prue-abcdefgh', 'p-prue-abcdefgh', 1201612430502010980, 14, 22, 12),
    ('c-shrek-abcdefgh', 'p-shrek-abcdefgh', 1201612479332110357, 15, 23, 13);

INSERT INTO Players (snowflake, name, discord_role_id, forum_user_id, confessional, tribe) VALUES
    ('p-aziah-abcdefgh', 'Aziah', 1201608872457142322, 6, 'c-aziah-abcdefgh', 't-voida-abcdefgh'),
    ('p-billy-abcdefgh', 'Billy', 1201608876542414848, 12, 'c-billy-abcdefgh', 't-cyclone-abcdefgh'),
    ('p-kingston-abcdefgh', 'Kingston', 1201608879721697322, 10, 'c-kingston-abcdefgh', 't-cyclone-abcdefgh'),
    ('p-lorelei-abcdefgh', 'Lorelei', 1201608883093917726, 5, 'c-lorelei-abcdefgh', 't-voida-abcdefgh'),
    ('p-nichelle-abcdefgh', 'Nichelle', 1201608886537425027, 7, 'c-nichelle-abcdefgh', 't-cyclone-abcdefgh'),
    ('p-oregano-abcdefgh', 'Oregano', 1201608889976758393, 11, 'c-oregano-abcdefgh', 't-voida-abcdefgh'),
    ('p-prue-abcdefgh', 'Prue', 1201608892933750815, 8, 'c-prue-abcdefgh', 't-cyclone-abcdefgh'),
    ('p-shrek-abcdefgh', 'Shrek', 1201608896289190038, 9, 'c-shrek-abcdefgh', 't-voida-abcdefgh');
