PRAGMA foreign_keys = ON;

CREATE TABLE participants(
  uniqname VARCHAR(20) NOT NULL,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP
);
