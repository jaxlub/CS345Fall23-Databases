CREATE TABLE Type (
  tconst   varchar(255) NOT NULL, 
  type     varchar(255) NOT NULL, 
  ordering int4 NOT NULL, 
  PRIMARY KEY (tconst, 
  type, 
  ordering));
CREATE TABLE akas (
  tconst          varchar(255) NOT NULL, 
  ordering        int4 NOT NULL, 
  region          varchar(255) NOT NULL, 
  language        varchar(255) NOT NULL, 
  title           varchar(255) NOT NULL, 
  isOriginalTitle bytea NOT NULL, 
  avg_rating      int4, 
  num_votes       int4, 
  PRIMARY KEY (tconst, 
  ordering));
CREATE TABLE Basics (
  tconst         varchar(255) NOT NULL, 
  titleType      varchar(255) NOT NULL, 
  primaryTitle   varchar(255) NOT NULL, 
  originalTitle  varchar(255) NOT NULL, 
  isAdult        bytea NOT NULL, 
  startYear      time(4) NOT NULL, 
  endYear        time(4), 
  runtimeMinutes int4 NOT NULL, 
  PRIMARY KEY (tconst));
CREATE TABLE Genres (
  tconst varchar(255) NOT NULL, 
  genre  varchar(255) NOT NULL, 
  PRIMARY KEY (tconst, 
  genre));
CREATE TABLE Writers (
  tconst varchar(255) NOT NULL, 
  writer varchar(255) NOT NULL, 
  PRIMARY KEY (tconst, 
  writer));
CREATE TABLE Director (
  tconst   varchar(255) NOT NULL, 
  director varchar(255) NOT NULL, 
  PRIMARY KEY (tconst, 
  director));
CREATE TABLE Episode (
  episode_tconst varchar(255) NOT NULL, 
  parentTconst   varchar(255) NOT NULL, 
  seasonNumber   int4 NOT NULL, 
  episode_number int4 NOT NULL, 
  PRIMARY KEY (episode_tconst, 
  parentTconst));
CREATE TABLE Entity (
  tconst   varchar(255) NOT NULL, 
  ordering int4 NOT NULL, 
  nconst   varchar(255) NOT NULL, 
  PRIMARY KEY (tconst, 
  ordering, 
  nconst));
CREATE TABLE Attributes (
  alt_title int4 NOT NULL, 
  tconst    varchar(255) NOT NULL, 
  ordering  int4 NOT NULL, 
  PRIMARY KEY (alt_title, 
  tconst, 
  ordering));
CREATE TABLE Job (
  nconst    varchar(255) NOT NULL, 
  tconst    varchar(255) NOT NULL, 
  ordering  int4 NOT NULL, 
  job       varchar(255), 
  catogory  varchar(255) NOT NULL, 
  character varchar(255), 
  PRIMARY KEY (nconst, 
  tconst, 
  ordering));
CREATE TABLE character_basics (
  nconst      varchar(255) NOT NULL, 
  primaryName varchar(255) NOT NULL, 
  birthYear   time(4) NOT NULL, 
  deathYear   time(4), 
  PRIMARY KEY (nconst));
CREATE TABLE PrimaryProfession (
  nconst     varchar(255) NOT NULL, 
  profession varchar(255) NOT NULL, 
  PRIMARY KEY (nconst, 
  profession));
CREATE TABLE KnownforTitles (
  nconst  varchar(255) NOT NULL, 
  tconsts varchar(255) NOT NULL, 
  PRIMARY KEY (nconst, 
  tconsts));
ALTER TABLE Genres ADD CONSTRAINT FKGenres280546 FOREIGN KEY (tconst) REFERENCES Basics (tconst);
ALTER TABLE akas ADD CONSTRAINT FKakas349442 FOREIGN KEY (tconst) REFERENCES Basics (tconst);
ALTER TABLE Episode ADD CONSTRAINT FKEpisode983330 FOREIGN KEY (parentTconst) REFERENCES Basics (tconst);
ALTER TABLE Attributes ADD CONSTRAINT FKAttributes514885 FOREIGN KEY (tconst, ordering) REFERENCES akas (tconst, ordering);
ALTER TABLE Type ADD CONSTRAINT FKType966087 FOREIGN KEY (tconst, ordering) REFERENCES akas (tconst, ordering);
ALTER TABLE PrimaryProfession ADD CONSTRAINT FKPrimaryPro190535 FOREIGN KEY (nconst) REFERENCES character_basics (nconst);
ALTER TABLE KnownforTitles ADD CONSTRAINT FKKnownforTi271472 FOREIGN KEY (nconst) REFERENCES character_basics (nconst);
ALTER TABLE Job ADD CONSTRAINT FKJob496830 FOREIGN KEY (nconst) REFERENCES character_basics (nconst);
ALTER TABLE Job ADD CONSTRAINT FKJob418440 FOREIGN KEY (tconst, ordering) REFERENCES akas (tconst, ordering);
ALTER TABLE KnownforTitles ADD CONSTRAINT FKKnownforTi204721 FOREIGN KEY (tconsts) REFERENCES Basics (tconst);
ALTER TABLE Writers ADD CONSTRAINT FKWriters956255 FOREIGN KEY (tconst) REFERENCES Basics (tconst);
ALTER TABLE Director ADD CONSTRAINT FKDirector41734 FOREIGN KEY (tconst) REFERENCES Basics (tconst);
