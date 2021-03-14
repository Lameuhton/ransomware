DROP TABLE if exists victims;
DROP TABLE if exists decrypted;
DROP TABLE if exists states;
DROP TABLE if exists encrypted;

CREATE TABLE victims (
    id_victim INT PRIMARY KEY NOT NULL,
    os VARCHAR(100),
    hash VARCHAR(100),
    disks VARCHAR(100),
    key VARCHAR(100)

);

CREATE TABLE decrypted (
    id_decrypted INT PRIMARY KEY NOT NULL,
    id_victim INT,
    datetime DATE,
    nb_file INT,
    FOREIGN KEY (id_victim) REFERENCES Victims(id_victim)

);

CREATE TABLE states (
    id_state INT PRIMARY KEY NOT NULL,
    id_victim INT,
    datetime DATE,
    nb_file INT,
    FOREIGN KEY (id_victim) REFERENCES Victims(id_victim)

);

CREATE TABLE encrypted (
    id_encrypted INT PRIMARY KEY NOT NULL,
    id_victim INT,
    datetime DATE,
    nb_file INT,
    FOREIGN KEY (id_victim) REFERENCES Victims(id_victim)

);