/*
This migration adds a new field (insert_date) which is the server's timestamps of the newly inserted dispensed event.
This is because the coffee-machine may reset it's date from time to time.

*/
CREATE TABLE jvm_dispensed_event_TEMP (
  id INTEGER PRIMARY KEY, 
  dispensed_date VARCHAR UNIQUE, 
  insert_date VARCHAR, 
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
  old.timestamp,
  old.timestamp,
  old.product_id,
  old.status,
  old.cost_coffee_beans,
  old.cost_milk,
  old.cost_choco,
  old.cost_sugar
FROM jvm_dispensed_event as old;


UPDATE jvm_dispensed_event_TEMP
SET insert_date = NULL
WHERE insert_date <= '2021-10-01 00:00:00';


DROP TABLE jvm_dispensed_event;


ALTER TABLE jvm_dispensed_event_TEMP RENAME TO jvm_dispensed_event;

 -- ALTERNATIVE:
 --ALTER TABLE jvm_dispensed_event RENAME COLUMN TIMESTAMP TO dispensed_date;
 --ALTER TABLE jvm_dispensed_event ADD insert_date VARCHAR;
 --UPDATE jvm_dispensed_event
--SET insert_date = dispensed_date
--WHERE insert_date IS NULL;