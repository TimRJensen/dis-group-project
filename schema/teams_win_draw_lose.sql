BEGIN;

ALTER TABLE teams
ADD COLUMN wins INTEGER,
ADD COLUMN draws INTEGER,
ADD COLUMN loses INTEGER,

COMMIT;