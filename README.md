# Specty
discord bot to test stuff.

## How to run?
You need PostgreSQL 9.5+

`1.`
Install dependencies `python3 -m pip install -U -r requirements.txt`

`2.`
```sql
CREATE ROLE specty WITH LOGIN PASSWORD 'some_password';
CREATE DATABASE specty OWNER specty;
```
`3.`
Fill `.env` file.
```
DISCORD_TOKEN=yourdiscordbottoken
LASTFM_KEY=yourlastfmapikey
LASTFM_SECRET=yourlastfmsecret
POSTGRESQL_USER=username
POSTGRESQL_HOST=localhost
POSTGRESQL_PASSWORD=yourpassword
```
`4`
Create database tables.
`5.`
Run using `python3 -B -m specty`