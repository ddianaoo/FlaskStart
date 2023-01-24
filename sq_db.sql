CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
id integer PRIMARY KEY AUTOINCREMENT,
title text NOT NULL,
text text NOT NULL,
url text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
id integer PRIMARY KEY AUTOINCREMENT,
username text NOT NULL,
email text NOT NULL,
password text NOT NULL,
photo BLOB DEFAULT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS messages (
id integer PRIMARY KEY AUTOINCREMENT,
email text NOT NULL,
message text NOT NULL,
time integer NOT NULL
);