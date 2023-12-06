DO
$$
BEGIN

CREATE EXTENSION IF NOT EXISTS pgcrypto;


CREATE TABLE IF NOT EXISTS bases
(
    "base" TEXT,
    "host" TEXT,
    "port" TEXT,
    "user" TEXT,
    "pass" TEXT,
    "ignore"  bool,
    PRIMARY KEY (base, host, port)
);

CREATE TABLE IF NOT EXISTS backups
(
    base TEXT,
    host TEXT,
    port TEXT,
    path TEXT,
    backupDate DATE,
    PRIMARY KEY (base, host, port, path)
);

END
$$