DROP TABLE if exists victims;
DROP TABLE if exists decrypted;
DROP TABLE if exists states;
DROP TABLE if exists encrypted;

CREATE TABLE victims (
    id_victim INTEGER PRIMARY KEY,
    hash VARCHAR(100),
    os VARCHAR(100),
    disks VARCHAR(100),
    key VARCHAR(100)

);

CREATE TABLE decrypted (
    id_decrypted INTEGER PRIMARY KEY,
    id_victim INTEGER,
    datetime TIMESTAMP NOT NULL DEFAULT(current_timestamp),
    nb_file INT,
    FOREIGN KEY (id_victim) REFERENCES Victims(id_victim)

);

CREATE TABLE states (
    id_state INTEGER PRIMARY KEY,
    id_victim INTEGER,
    datetime TIMESTAMP NOT NULL DEFAULT(current_timestamp),
    state INT,
    FOREIGN KEY (id_victim) REFERENCES Victims(id_victim)
);

CREATE TABLE encrypted (
    id_encrypted INTEGER PRIMARY KEY,
    id_victim INTEGER,
    datetime TIMESTAMP NOT NULL DEFAULT(current_timestamp),
    nb_file INT,
    FOREIGN KEY (id_victim) REFERENCES Victims(id_victim)

);