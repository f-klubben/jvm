UPDATE jvm_dispensed_event
SET insert_date = dispensed_date
WHERE dispensed_date >= '2021-01-01 00:00:00.00';


UPDATE jvm_fill_event
SET insert_date = fill_date
WHERE fill_date >= '2021-01-01 00:00:00.00';


UPDATE jvm_ingredient_level
SET insert_date = level_date
WHERE level_date >= '2021-01-01 00:00:00.00';

 -- Fix the dates on records because the coffee machine's clock reset in that time frame..

UPDATE jvm_dispensed_event
SET insert_date = strftime('%Y-%m-%d %H:%M:%f', datetime(dispensed_date, '194845 hours'))
WHERE dispensed_date < '2000-01-01 00:00:00.00';


UPDATE jvm_ingredient_level
SET insert_date = strftime('%Y-%m-%d %H:%M:%f', datetime(level_date, '194845 hours'))
WHERE level_date BETWEEN '1998-01-01 00:00:00.00' AND '2021-01-01 00:00:00.00';


UPDATE jvm_ingredient_level
SET insert_date = strftime('%Y-%m-%d %H:%M:%f', datetime(level_date, '191080 hours'))
WHERE level_date BETWEEN '1998-01-01 00:00:00.00' AND '2021-01-01 00:00:00.00'
  AND id < 20;


UPDATE jvm_fill_event
SET insert_date = strftime('%Y-%m-%d %H:%M:%f', datetime(fill_date, '194845 hours'))
WHERE fill_date BETWEEN '1998-01-01 00:00:00.00' AND '2021-01-01 00:00:00.00';