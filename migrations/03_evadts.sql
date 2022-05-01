CREATE TABLE jvm_evadts (
  id INTEGER PRIMARY KEY, dispenser_date VARCHAR UNIQUE, 
  server_date VARCHAR, coffee_beans INTEGER, 
  milk_product INTEGER, sugar INTEGER, 
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
