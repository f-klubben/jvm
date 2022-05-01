CREATE TABLE jvm_evadts (
  id INTEGER PRIMARY KEY,
  dispenser_date VARCHAR UNIQUE,
  server_date VARCHAR DEFAULT (strftime('%Y-%m-%d %H:%M:%S.%f', 'now')),
  coffee_beans INTEGER,
  milk_product INTEGER,
  sugar INTEGER,
  chocolate INTEGER
);

CREATE TABLE jvm_notification (
  id INTEGER PRIMARY KEY, ingredient VARCHAR UNIQUE,
  last_notif VARCHAR, last_notif_ts VARCHAR
);

INSERT INTO jvm_notification (
  id, ingredient, last_notif, last_notif_ts
)
VALUES
  (0, 'Coffee Beans', '1970-01-01 00:00:00.000000', '42.69'),
  (1, 'Chocolate', '1970-01-01 00:00:00.000000', '42.69'),
  (2, 'Milk product', '1970-01-01 00:00:00.000000', '42.69'),
  (3, 'Sugar', '1970-01-01 00:00:00.000000', '42.69');


CREATE TABLE jvm_dispensed_event_TEMP (
  id INTEGER PRIMARY KEY,
  dispensed_date VARCHAR UNIQUE,
  insert_date VARCHAR DEFAULT (strftime('%Y-%m-%d %H:%M:%S.%f', 'now')),
  product_id INTEGER,
  status VARCHAR,
  cost_coffee_beans DEICMAL(10,5),
  cost_milk DECIMAL(10,5),
  cost_choco DECIMAL(10,5),
  cost_sugar DECIMAL(10,5)
);

INSERT INTO jvm_dispensed_event_TEMP
SELECT
  old.id,
  old.dispensed_date,
  old.insert_date,
  old.product_id,
  old.status,
  old.cost_coffee_beans,
  old.cost_milk,
  old.cost_choco,
  old.cost_sugar
FROM jvm_dispensed_event as old;

DROP TABLE jvm_dispensed_event;

ALTER TABLE jvm_dispensed_event_TEMP RENAME TO jvm_dispensed_event;

CREATE TABLE jvm_fill_event_TEMP (
  id INTEGER PRIMARY KEY,
  fill_date VARCHAR UNIQUE,
  insert_date VARCHAR DEFAULT (strftime('%Y-%m-%d %H:%M:%S.%f', 'now')),
  ingredient VARCHAR,
  value INTEGER
);

INSERT INTO jvm_fill_event_TEMP
SELECT
  old.id,
  old.fill_date,
  old.insert_date,
  old.ingredient,
  old.value
FROM jvm_fill_event as old;

DROP TABLE jvm_fill_event;

ALTER TABLE jvm_fill_event_TEMP RENAME TO jvm_fill_event;

CREATE TABLE jvm_ingredient_level_TEMP (
  id INTEGER PRIMARY KEY,
  level_date VARCHAR UNIQUE,
  insert_date VARCHAR DEFAULT (strftime('%Y-%m-%d %H:%M:%S.%f', 'now')),
  ingredient VARCHAR,
  value INTEGER
);

INSERT INTO jvm_ingredient_level_TEMP
SELECT
  old.id,
  old.level_date,
  old.insert_date,
  old.ingredient,
  old.value
FROM jvm_ingredient_level as old;

DROP TABLE jvm_ingredient_level;

ALTER TABLE jvm_ingredient_level_TEMP RENAME TO jvm_ingredient_level;
