from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from datetime import datetime
import sqlite3

PRODUCT_STMT = """
SELECT localized_name,
       cost_coffee_beans,
       cost_choco,
       cost_milk,
       cost_sugar,
       number_dispensed
FROM jvm_product
ORDER BY localized_name ASC
"""

RECENT_STATS = """
SELECT p.localized_name,
       COUNT(de.product_id)
FROM jvm_product AS p
JOIN jvm_dispensed_event AS de ON de.product_id = p.id
WHERE insert_date >= date('now', '-1 month')
GROUP BY p.localized_name
ORDER BY COUNT(de.product_id) DESC
"""

GENERAL_INFO = """
SELECT last_cleaned,
       initialization_date,
       total_prod_dispensed,
       coffee_beans_dispensed / (1000 * 10.0),
       milk_dispensed / (1000 * 10.0),
       choco_dispensed / (1000 * 10.0)
FROM jvm_info
"""

INGREDIENT_ESTIMATE = """
SELECT id,
       localized_name,
       estimate_fill_level,
       max_level
FROM jvm_ingredient_estimate
ORDER BY id ASC
"""

MOST_RECENT_DISPENSE = """
SELECT id,
       strftime("%Y-%m-%d %H:%M:%S", insert_date)
FROM jvm_dispensed_event
ORDER BY id DESC LIMIT 1
"""


CURR_DIR = Path(__file__).parent.resolve()


def reformat_statistics_output(res):
    result = [["" for i in range(7 + 1)] for j in range(4)]
    result[0][0] = "Produkt"
    rows = {"Header": 0}
    columns = {"Produkt": 0}
    # res = []
    for column_name in res.keys():
        (timename, productname) = column_name.split("|")
        (count, start, end) = res[column_name].split("|")

        if timename not in columns:
            columns[timename] = len(columns.keys())
        if productname not in rows:
            rows[productname] = len(rows.keys())

        row_index = rows[productname]
        column_index = columns[timename]

        result[row_index][column_index] = int(count)
        result[row_index][0] = productname
        result[0][column_index] = (timename, start, end)
    return result


def generate_coffee_report(sqlite_path: str):
    con = sqlite3.connect(str(sqlite_path))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute(PRODUCT_STMT)
    products = cur.fetchall()
    cur.execute(RECENT_STATS)
    recents = cur.fetchall()
    cur.execute(GENERAL_INFO)
    general = cur.fetchone()
    cur.execute(INGREDIENT_ESTIMATE)
    ingredients = cur.fetchall()
    cur.execute(MOST_RECENT_DISPENSE)
    recent_dispense = cur.fetchone()
    statistics_file = CURR_DIR / "historic_statistics.sql"
    with open(statistics_file, mode="r", encoding="utf-8") as sql_file:
        statement = sql_file.read()
        cur.execute(statement)
        row = cur.fetchone()

        historic_statistics = reformat_statistics_output(row)
    templates_path = CURR_DIR / "templates"
    env = Environment(loader=FileSystemLoader(templates_path))
    template = env.get_template("index.html")

    html_path = CURR_DIR / "html" / "index.html"
    with open(html_path, mode="wb") as file:
        file.write(
            template.render(
                name="Kaffe",
                update_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                products=products,
                recents=recents,
                general=general,
                ingredients=ingredients,
                recent_dispense=recent_dispense,
                historic_statistics=historic_statistics,
            ).encode("utf-8")
        )


if __name__ == "__main__":
    sqlite_path = str(Path(__file__ + "/../../db.sqlite3").resolve())
    generate_coffee_report(sqlite_path)
