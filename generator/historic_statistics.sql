/*
The following Python3 code generated the underlying SQL statement.
The idea is to fetch statistics according to the different product categories and a timeframe.
Results from the statement generated is like the following (but transposed(meaning, columns are rows)):
+-------------------------+----------------------------------------------+
| I dag|Kakao             | 11|2022-03-23 00:00:00|2022-03-23 23:59:59   |
+-------------------------+----------------------------------------------+
| Denne uge|Kakao         | 39|2022-03-21 00:00:00|2022-03-27 23:59:59   |
+-------------------------+----------------------------------------------+
| Sidste uge|Kakao        | 66|2022-03-14 00:00:00|2022-03-20 23:59:59   |
+-------------------------+----------------------------------------------+
| Denne måned|Kakao       | 197|2022-03-01 00:00:00|2022-03-31 23:59:59  |
+-------------------------+----------------------------------------------+
| Sidste måned|Kakao      | 137|2022-02-01 00:00:00|2022-02-28 23:59:59  |
+-------------------------+----------------------------------------------+
| Dette år|Kakao          | 348|2022-01-01 00:00:00|2022-12-31 23:59:59  |
+-------------------------+----------------------------------------------+
| Sidste år|Kakao         | 390|2021-01-01 00:00:00|2021-12-31 23:59:59  |
+-------------------------+----------------------------------------------+
| I dag|Varmt vand        | 23|2022-03-23 00:00:00|2022-03-23 23:59:59   |
+-------------------------+----------------------------------------------+
| Denne uge|Varmt vand    | 73|2022-03-21 00:00:00|2022-03-27 23:59:59   |
+-------------------------+----------------------------------------------+
| Sidste uge|Varmt vand   | 107|2022-03-14 00:00:00|2022-03-20 23:59:59  |
+-------------------------+----------------------------------------------+
| Denne måned|Varmt vand  | 287|2022-03-01 00:00:00|2022-03-31 23:59:59  |
+-------------------------+----------------------------------------------+
| Sidste måned|Varmt vand | 221|2022-02-01 00:00:00|2022-02-28 23:59:59  |
+-------------------------+----------------------------------------------+
| Dette år|Varmt vand     | 541|2022-01-01 00:00:00|2022-12-31 23:59:59  |
+-------------------------+----------------------------------------------+
| Sidste år|Varmt vand    | 1026|2021-01-01 00:00:00|2021-12-31 23:59:59 |
+-------------------------+----------------------------------------------+
| I dag|Kaffe             | 55|2022-03-23 00:00:00|2022-03-23 23:59:59   |
+-------------------------+----------------------------------------------+
| Denne uge|Kaffe         | 186|2022-03-21 00:00:00|2022-03-27 23:59:59  |
+-------------------------+----------------------------------------------+
| Sidste uge|Kaffe        | 282|2022-03-14 00:00:00|2022-03-20 23:59:59  |
+-------------------------+----------------------------------------------+
| Denne måned|Kaffe       | 815|2022-03-01 00:00:00|2022-03-31 23:59:59  |
+-------------------------+----------------------------------------------+
| Sidste måned|Kaffe      | 597|2022-02-01 00:00:00|2022-02-28 23:59:59  |
+-------------------------+----------------------------------------------+
| Dette år|Kaffe          | 1454|2022-01-01 00:00:00|2022-12-31 23:59:59 |
+-------------------------+----------------------------------------------+
| Sidste år|Kaffe         | 2022|2021-01-01 00:00:00|2021-12-31 23:59:59 |
+-------------------------+----------------------------------------------+

COLUMN_CLAUSES = [
    (
        "datetime(date('now'))",
        "datetime(date('now', '+1 days'), '-1 seconds')",
        "I dag",
    ),
    (
        "datetime(date('now'), '-6 days', 'weekday 1')",
        "datetime(date('now'), '-1 days', 'weekday 1', '-1 seconds')",
        "Denne uge",
    ),
    (
        "datetime(date('now'), '-13 days', 'weekday 1')",
        "datetime(date('now'), '-8 days', 'weekday 1', '-1 seconds')",
        "Sidste uge",
    ),
    (
        "datetime(date('now'), 'start of month')",
        "datetime(date('now'), '+1 months', 'start of month', '-1 seconds')",
        "Denne måned",
    ),
    (
        "datetime(date('now'), '-1 months', 'start of month')",
        "datetime(date('now'), 'start of month', '-1 seconds')",
        "Sidste måned",
    ),
    (
        "datetime(date('now'), 'start of year')",
        "datetime(date('now'), '+1 years', 'start of year', '-1 seconds')",
        "Dette år",
    ),
    (
        "datetime(date('now'), '-1 years', 'start of year')",
        "datetime(date('now'), 'start of year', '-1 seconds')",
        "Sidste år",
    ),
]
ROW_CLAUSES = [
    ("product_id IN (20,21)", "Kakao"),
    ("product_id = 23", "Varmt vand"),
    ("product_id NOT IN (20,21,23)", "Kaffe"),
]
columns = []
for row_clause in ROW_CLAUSES:
  for column_clause in COLUMN_CLAUSES:
    between_stmt = (
      f"insert_date BETWEEN {column_clause[0]} AND {column_clause[1]}"
    )
    column_name = "|".join([column_clause[2], row_clause[1]])
    sub_stmt = f"(SELECT COUNT(*) || '|' || {column_clause[0]} || '|' || {column_clause[1]} FROM jvm_dispensed_event WHERE {row_clause[0]} AND {between_stmt}) as '{column_name}'"
    columns.append(sub_stmt)
columns_str = ", ".join(columns)
str_lab = f"SELECT {columns_str};"
print(str_lab)

*/

SELECT
  (SELECT COUNT(*) || '|' || datetime(date('now')) || '|' || datetime(date('now', '+1 days'), '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id IN (20,
                        21)
     AND insert_date BETWEEN datetime(date('now')) AND datetime(date('now', '+1 days'), '-1 seconds')) AS 'I dag|Kakao',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-6 days', 'weekday 1') || '|' || datetime(date('now'), '-1 days', 'weekday 1', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id IN (20,
                        21)
     AND insert_date BETWEEN datetime(date('now'), '-6 days', 'weekday 1') AND datetime(date('now'), '-1 days', 'weekday 1', '-1 seconds')) AS 'Denne uge|Kakao',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-13 days', 'weekday 1') || '|' || datetime(date('now'), '-8 days', 'weekday 1', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id IN (20,
                        21)
     AND insert_date BETWEEN datetime(date('now'), '-13 days', 'weekday 1') AND datetime(date('now'), '-8 days', 'weekday 1', '-1 seconds')) AS 'Sidste uge|Kakao',

  (SELECT COUNT(*) || '|' || datetime(date('now'), 'start of month') || '|' || datetime(date('now'), '+1 months', 'start of month', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id IN (20,
                        21)
     AND insert_date BETWEEN datetime(date('now'), 'start of month') AND datetime(date('now'), '+1 months', 'start of month', '-1 seconds')) AS 'Denne måned|Kakao',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-1 months', 'start of month') || '|' || datetime(date('now'), 'start of month', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id IN (20,
                        21)
     AND insert_date BETWEEN datetime(date('now'), '-1 months', 'start of month') AND datetime(date('now'), 'start of month', '-1 seconds')) AS 'Sidste måned|Kakao',

  (SELECT COUNT(*) || '|' || datetime(date('now'), 'start of year') || '|' || datetime(date('now'), '+1 years', 'start of year', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id IN (20,
                        21)
     AND insert_date BETWEEN datetime(date('now'), 'start of year') AND datetime(date('now'), '+1 years', 'start of year', '-1 seconds')) AS 'Dette år|Kakao',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-1 years', 'start of year') || '|' || datetime(date('now'), 'start of year', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id IN (20,
                        21)
     AND insert_date BETWEEN datetime(date('now'), '-1 years', 'start of year') AND datetime(date('now'), 'start of year', '-1 seconds')) AS 'Sidste år|Kakao',

  (SELECT COUNT(*) || '|' || datetime(date('now')) || '|' || datetime(date('now', '+1 days'), '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id = 23
     AND insert_date BETWEEN datetime(date('now')) AND datetime(date('now', '+1 days'), '-1 seconds')) AS 'I dag|Varmt vand',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-6 days', 'weekday 1') || '|' || datetime(date('now'), '-1 days', 'weekday 1', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id = 23
     AND insert_date BETWEEN datetime(date('now'), '-6 days', 'weekday 1') AND datetime(date('now'), '-1 days', 'weekday 1', '-1 seconds')) AS 'Denne uge|Varmt vand',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-13 days', 'weekday 1') || '|' || datetime(date('now'), '-8 days', 'weekday 1', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id = 23
     AND insert_date BETWEEN datetime(date('now'), '-13 days', 'weekday 1') AND datetime(date('now'), '-8 days', 'weekday 1', '-1 seconds')) AS 'Sidste uge|Varmt vand',

  (SELECT COUNT(*) || '|' || datetime(date('now'), 'start of month') || '|' || datetime(date('now'), '+1 months', 'start of month', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id = 23
     AND insert_date BETWEEN datetime(date('now'), 'start of month') AND datetime(date('now'), '+1 months', 'start of month', '-1 seconds')) AS 'Denne måned|Varmt vand',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-1 months', 'start of month') || '|' || datetime(date('now'), 'start of month', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id = 23
     AND insert_date BETWEEN datetime(date('now'), '-1 months', 'start of month') AND datetime(date('now'), 'start of month', '-1 seconds')) AS 'Sidste måned|Varmt vand',

  (SELECT COUNT(*) || '|' || datetime(date('now'), 'start of year') || '|' || datetime(date('now'), '+1 years', 'start of year', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id = 23
     AND insert_date BETWEEN datetime(date('now'), 'start of year') AND datetime(date('now'), '+1 years', 'start of year', '-1 seconds')) AS 'Dette år|Varmt vand',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-1 years', 'start of year') || '|' || datetime(date('now'), 'start of year', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id = 23
     AND insert_date BETWEEN datetime(date('now'), '-1 years', 'start of year') AND datetime(date('now'), 'start of year', '-1 seconds')) AS 'Sidste år|Varmt vand',

  (SELECT COUNT(*) || '|' || datetime(date('now')) || '|' || datetime(date('now', '+1 days'), '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id NOT IN (20,
                            21,
                            23)
     AND insert_date BETWEEN datetime(date('now')) AND datetime(date('now', '+1 days'), '-1 seconds')) AS 'I dag|Kaffe',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-6 days', 'weekday 1') || '|' || datetime(date('now'), '-1 days', 'weekday 1', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id NOT IN (20,
                            21,
                            23)
     AND insert_date BETWEEN datetime(date('now'), '-6 days', 'weekday 1') AND datetime(date('now'), '-1 days', 'weekday 1', '-1 seconds')) AS 'Denne uge|Kaffe',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-13 days', 'weekday 1') || '|' || datetime(date('now'), '-8 days', 'weekday 1', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id NOT IN (20,
                            21,
                            23)
     AND insert_date BETWEEN datetime(date('now'), '-13 days', 'weekday 1') AND datetime(date('now'), '-8 days', 'weekday 1', '-1 seconds')) AS 'Sidste uge|Kaffe',

  (SELECT COUNT(*) || '|' || datetime(date('now'), 'start of month') || '|' || datetime(date('now'), '+1 months', 'start of month', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id NOT IN (20,
                            21,
                            23)
     AND insert_date BETWEEN datetime(date('now'), 'start of month') AND datetime(date('now'), '+1 months', 'start of month', '-1 seconds')) AS 'Denne måned|Kaffe',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-1 months', 'start of month') || '|' || datetime(date('now'), 'start of month', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id NOT IN (20,
                            21,
                            23)
     AND insert_date BETWEEN datetime(date('now'), '-1 months', 'start of month') AND datetime(date('now'), 'start of month', '-1 seconds')) AS 'Sidste måned|Kaffe',

  (SELECT COUNT(*) || '|' || datetime(date('now'), 'start of year') || '|' || datetime(date('now'), '+1 years', 'start of year', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id NOT IN (20,
                            21,
                            23)
     AND insert_date BETWEEN datetime(date('now'), 'start of year') AND datetime(date('now'), '+1 years', 'start of year', '-1 seconds')) AS 'Dette år|Kaffe',

  (SELECT COUNT(*) || '|' || datetime(date('now'), '-1 years', 'start of year') || '|' || datetime(date('now'), 'start of year', '-1 seconds')
   FROM jvm_dispensed_event
   WHERE product_id NOT IN (20,
                            21,
                            23)
     AND insert_date BETWEEN datetime(date('now'), '-1 years', 'start of year') AND datetime(date('now'), 'start of year', '-1 seconds')) AS 'Sidste år|Kaffe';