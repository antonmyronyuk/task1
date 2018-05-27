-- Initialize the database.
-- Drop any existing data and create empty tables.

DROP TABLE IF EXISTS notes;

CREATE TABLE notes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  text TEXT NOT NULL,
  unique_count INTEGER
);

-- for fast sorting
CREATE INDEX unique_count_index
ON notes (unique_count);
