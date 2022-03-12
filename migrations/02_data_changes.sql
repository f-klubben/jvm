-- Create a new ingredient level table.
CREATE TABLE jvm_ingredient_level (
  id INTEGER PRIMARY KEY,
  level_date VARCHAR UNIQUE,
  insert_date VARCHAR,
  ingredient VARCHAR,
  value INTEGER
);

-- Fill default values into the table
INSERT INTO jvm_ingredient_level
  (level_date, insert_date, ingredient, value)
VALUES
  ('1970-01-01 00:00:00.000000', '1970-01-01 00:00:00.000000', 'Coffee Beans', 0),
  ('1970-01-01 00:00:00.000001', '1970-01-01 00:00:00.000000', 'Chocolate', 0),
  ('1970-01-01 00:00:00.000002', '1970-01-01 00:00:00.000000', 'Milk product', 0),
  ('1970-01-01 00:00:00.000003', '1970-01-01 00:00:00.000000', 'Sugar', 0);

-- Fill old values into the table
INSERT INTO jvm_ingredient_level
  (level_date, insert_date, ingredient, value)
SELECT choco_filldate, choco_filldate, 'Chocolate', choco_fill
FROM jvm_info;


INSERT INTO jvm_ingredient_level
  (level_date, insert_date, ingredient, value)
SELECT coffee_beans_filldate, coffee_beans_filldate, 'Coffee Beans', coffee_beans_fill
FROM jvm_info;


INSERT INTO jvm_ingredient_level
  (level_date, insert_date, ingredient, value)
SELECT milk_filldate, milk_filldate, 'Milk product', milk_fill
FROM jvm_info;


INSERT INTO jvm_ingredient_level
  (level_date, insert_date, ingredient, value)
SELECT sugar_filldate, sugar_filldate, 'Sugar', sugar_fill
FROM jvm_info;

-- Remove old columns
ALTER TABLE jvm_info
DROP COLUMN choco_fill;


ALTER TABLE jvm_info
DROP COLUMN choco_filldate;


ALTER TABLE jvm_info
DROP COLUMN coffee_beans_fill;


ALTER TABLE jvm_info
DROP COLUMN coffee_beans_filldate;


ALTER TABLE jvm_info
DROP COLUMN milk_fill;


ALTER TABLE jvm_info
DROP COLUMN milk_filldate;


ALTER TABLE jvm_info
DROP COLUMN sugar_fill;


ALTER TABLE jvm_info
DROP COLUMN sugar_filldate;

-- Remove old ingredient estimate table
DROP TABLE jvm_ingredient_estimate;

-- Create new ingredient estimate table
CREATE TABLE jvm_ingredient_estimate (
  id INTEGER PRIMARY KEY,
  estimate_fill_level INTEGER,
  ingredient VARCHAR UNIQUE,
  localized_name VARCHAR,
  max_level INTEGER
);

-- Input default values
INSERT INTO jvm_ingredient_estimate
  (id, ingredient, estimate_fill_level, max_level, localized_name)
VALUES
  (0, 'Coffee Beans', 0, 2400, 'Kaffebønner'),
  (1, 'Chocolate', 0, 2200, 'Chokolade'),
  (2, 'Milk product', 0, 1800, 'Mælkeprodukt'),
  (3, 'Sugar', 0, 2400, 'Sukker');

-- Create new fill table
CREATE TABLE jvm_fill_event_TEMP (
  id INTEGER PRIMARY KEY,
  fill_date VARCHAR UNIQUE,
  ingredient VARCHAR,
  insert_date VARCHAR,
  value INTEGER
);

-- Copy old values into the table
INSERT INTO jvm_fill_event_TEMP
SELECT
  old.id,
  old.timestamp,
  old.ingredient,
  old.timestamp,
  old.value
FROM
  jvm_fill_event as old;

-- Remove old table
DROP TABLE jvm_fill_event;

-- Rename new table to the actual name
ALTER TABLE jvm_fill_event_TEMP RENAME TO jvm_fill_event;

-- Fix datetimes of data in the database
UPDATE jvm_fill_event
SET insert_date = strftime('%Y-%m-%d %H:%M:%f', datetime(fill_date, '194845 hours'))
WHERE fill_date BETWEEN '1998-01-01 00:00:00.00' AND '2021-01-01 00:00:00.00';