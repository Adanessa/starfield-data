PRAGMA foreign_keys = ON;

CREATE TABLE resource_rarities (
  rarity TEXT PRIMARY KEY
);

INSERT INTO resource_rarities VALUES ('common');
INSERT INTO resource_rarities VALUES ('uncommon');
INSERT INTO resource_rarities VALUES ('rare');
INSERT INTO resource_rarities VALUES ('exotic');
INSERT INTO resource_rarities VALUES ('unique');


CREATE TABLE resource_types (
  type TEXT PRIMARY KEY
);

INSERT INTO resource_types VALUES ('organic');
INSERT INTO resource_types VALUES ('inorganic');
INSERT INTO resource_types VALUES ('manufactured');


CREATE TABLE resources (
  name TEXT PRIMARY KEY,
  shortName TEXT NOT NULL,
  rarity TEXT NOT NULL,
  type TEXT NOT NULL,
  mass REAL NOT NULL,
  value INT NOT NULL,
  value_to_mass INT NOT NULL,
  FOREIGN KEY(rarity) REFERENCES resource_rarities(rarity),
  FOREIGN KEY(type) REFERENCES resource_types(type)
);

CREATE TABLE systems (
  name TEXT PRIMARY KEY,
  body_count INT
);


CREATE TABLE bodies (
  name TEXT PRIMARY KEY,
  system TEXT NOT NULL,
  type TEXT NOT NULL,
  gravity REAL NOT NULL,
  temperature TEXT NOT NULL,
  atmosphere TEXT NOT NULL,
  magnetosphere TEXT NOT NULL,
  water INT NOT NULL,
  fauna_count INT NOT NULL,
  flora_count INT NOT NULL,
  hab_rank INT NOT NULL,
  day_length INT NOT NULL,
  FOREIGN KEY(system) REFERENCES systems(name)
);


CREATE TABLE biomes (
  system TEXT NOT NULL,
  body TEXT NOT NULL,
  type TEXT NOT NULL,
  coverage STRING NOT NULL,
  FOREIGN KEY(system) REFERENCES systems(name),
  FOREIGN KEY(body) REFERENCES bodies(name)
);


CREATE TABLE traits (
  system TEXT NOT NULL,
  body TEXT NOT NULL,
  type TEXT NOT NULL,
  FOREIGN KEY(system) REFERENCES systems(name),
  FOREIGN KEY(body) REFERENCES bodies(name)  
);


CREATE TABLE body_resources (
  system TEXT NOT NULL,
  body TEXT NOT NULL,
  resource TEXT NOT NULL,
  FOREIGN KEY(system) REFERENCES systems(name),
  FOREIGN KEY(body) REFERENCES bodies(name),
  FOREIGN KEY(resource) REFERENCES resources(name)
);


CREATE TABLE body_organics (
  system TEXT NOT NULL,
  body TEXT NOT NULL,
  organism TEXT NOT NULL,
  resource TEXT NOT NULL,
  domesticable INT NOT NULL,
  FOREIGN KEY(system) REFERENCES systems(name),
  FOREIGN KEY(body) REFERENCES bodies(name),
  FOREIGN KEY(resource) REFERENCES resources(name)  
);
