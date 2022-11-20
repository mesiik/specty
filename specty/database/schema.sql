CREATE TABLE IF NOT EXISTS prefixes(
    guild_id BIGINT PRIMARY KEY NOT NULL, 
    prefix TEXT DEFAULT (';')
    );
CREATE TABLE IF NOT EXISTS lastfm(
    user_id BIGINT PRIMARY KEY NOT NULL, 
    username TEXT
);
