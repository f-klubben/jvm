import sqlite3
import os
from models import Product, DispensedEvent, FillEvent, DispenserInfo, IngredientLevel
from datetime import datetime, timedelta
from decimal import Decimal
from config import get_db_file
from pathlib import Path

CURR_DIR = Path(__file__).parent.resolve()
DB_FILE_NAME = CURR_DIR / get_db_file()

DISPENSED_EVENT_TABLE = "jvm_dispensed_event"
PRODUCT_TABLE = "jvm_product"
DISPENSER_INFO_TABLE = "jvm_info"
INGREDIENT_ESTIMATE_TABLE = "jvm_ingredient_estimate"
FILL_EVENT_TABLE = "jvm_fill_event"
INGREDIENT_LEVEL_TABLE = "jvm_ingredient_level"


def create_db_conn():
    if os.path.exists(DB_FILE_NAME):
        conn = sqlite3.connect(str(DB_FILE_NAME))
    else:
        conn = sqlite3.connect(str(DB_FILE_NAME))
        setup_database(conn)
    conn.row_factory = sqlite3.Row
    return conn


# For usage in test
def get_sqlite_database():
    return DB_FILE_NAME


def setup_database(conn):
    cur = conn.cursor()
    # Setup the database

    # Products
    cur.execute(
        f"""CREATE TABLE {PRODUCT_TABLE} (
              id INTEGER PRIMARY KEY,
              name VARCHAR UNIQUE,
              cost_coffee_beans DECIMAL(10,5),
              cost_milk DECIMAL(10,5),
              cost_choco DECIMAL(10,5),
              cost_sugar DECIMAL(10,5),
              sold_out_last VARCHAR,
              number_dispensed INTEGER,
              price INTEGER,
              product_index INTEGER,
              product_identifier VARCHAR,
              localized_name VARCHAR UNIQUE
        )"""
    )

    default_products_file = "default.json"
    if os.path.exists(default_products_file):
        with open(default_products_file, "r") as f:
            import json

            default_products = json.load(f)
        query = f"""
        INSERT INTO {PRODUCT_TABLE}
          (name, cost_coffee_beans, cost_milk, cost_choco, cost_sugar, localized_name)
        VALUES
          (?, ?, ?, ?, ?, ?)
      """
        rows = [
            (
                p["name"],
                p["coffee_cost"],
                p["milk_cost"],
                p["sugar_cost"],
                p["choco_cost"],
                p["localized_name"] if p["localized_name"] != "" else None,
            )
            for p in default_products
        ]
        cur.executemany(query, rows)

    # Dispensed events
    cur.execute(
        f"""CREATE TABLE {DISPENSED_EVENT_TABLE} (
              id INTEGER PRIMARY KEY,
              dispensed_date VARCHAR UNIQUE,
              insert_date VARCHAR,
              product_id INTEGER,
              status VARCHAR,
              cost_coffee_beans DEICMAL(10,5),
              cost_milk DECIMAL(10,5),
              cost_choco DECIMAL(10,5),
              cost_sugar DECIMAL(10,5)
        )"""
    )
    # General info
    cur.execute(
        f"""CREATE TABLE {DISPENSER_INFO_TABLE} (
              id INTEGER PRIMARY KEY,
              last_cleaned VARCHAR,
              initialization_date VARCHAR,
              total_prod_dispensed INTEGER,
              coffee_beans_dispensed INTEGER,
              milk_dispensed INTEGER,
              choco_dispensed INTEGER,
              sugar_dispensed INTEGER
        )"""
    )
    cur.execute(
        f"""INSERT INTO {DISPENSER_INFO_TABLE}
      (id)
    VALUES
      (0)"""
    )

    # Estimates
    cur.execute(
        f"""CREATE TABLE {INGREDIENT_ESTIMATE_TABLE} (
              id INTEGER PRIMARY KEY,
              ingredient VARCHAR UNIQUE,
              estimate_fill_level INTEGER,
              max_level INTEGER,
              localized_name VARCHAR
        )"""
    )
    cur.execute(
        f"""INSERT INTO {INGREDIENT_ESTIMATE_TABLE} 
              (id, ingredient, estimate_fill_level, max_level, localized_name) 
        VALUES 
              (0, 'Coffee Beans', 0, 2400, 'Kaffebønner'),
              (1, 'Chocolate', 0, 2200, 'Chokolade'),
              (2, 'Milk product', 0, 1800, 'Mælkeprodukt'),
              (3, 'Sugar', 0, 2400, 'Sukker')
        """
    )

    # Fill events
    cur.execute(
        f"""CREATE TABLE {FILL_EVENT_TABLE} (
              id INTEGER PRIMARY KEY,
              fill_date VARCHAR UNIQUE,
              insert_date VARCHAR,
              ingredient VARCHAR,
              value INTEGER
        )"""
    )

    # Fill levels
    cur.execute(
        f"""CREATE TABLE {INGREDIENT_LEVEL_TABLE} (
            id INTEGER PRIMARY KEY,
            level_date VARCHAR UNIQUE,
            insert_date VARCHAR,
            ingredient VARCHAR,
            value INTEGER
        )"""
    )
    cur.execute(
        f"""INSERT INTO {INGREDIENT_LEVEL_TABLE} 
            (level_date, insert_date, ingredient, value) 
        VALUES 
            ('1970-01-01 00:00:00.000000', '1970-01-01 00:00:00.000000', 'Coffee Beans', 0),
            ('1970-01-01 00:00:00.000001', '1970-01-01 00:00:00.000000', 'Chocolate', 0),
            ('1970-01-01 00:00:00.000002', '1970-01-01 00:00:00.000000', 'Milk product', 0),
            ('1970-01-01 00:00:00.000003', '1970-01-01 00:00:00.000000', 'Sugar', 0)
        """
    )

    cur.close()
    conn.commit()


def insert_dispensed_drink_event(conn, d: DispensedEvent, p: Product):
    # insert the dispensed event into the database
    cur = conn.cursor()
    query = f"""INSERT OR IGNORE INTO {DISPENSED_EVENT_TABLE}
      (dispensed_date, insert_date, product_id, status, cost_coffee_beans, cost_milk, cost_choco, cost_sugar)
    VALUES
      (?, ?, ?, ?, ?, ?, ?, ?)"""
    cur.execute(
        query,
        (
            d.dispensed_date,
            d.insert_date,
            p.id,
            d.status,
            p.cost_coffee_beans,
            p.cost_milk,
            p.cost_choco,
            p.cost_sugar,
        ),
    )
    conn.commit()


def get_products(conn):
    cur = conn.cursor()
    query = f"""
    SELECT
      id,
      name,
      cost_coffee_beans,
      cost_milk,
      cost_choco,
      cost_sugar,
      sold_out_last,
      number_dispensed,
      price,
      product_index,
      product_identifier,
      localized_name
    FROM
      {PRODUCT_TABLE}
  """
    cur.execute(query)
    rows = cur.fetchall()
    return [
        Product(
            id=r["id"],
            name=r["name"],
            cost_coffee_beans=r["cost_coffee_beans"],
            cost_milk=r["cost_milk"],
            cost_choco=r["cost_choco"],
            cost_sugar=r["cost_sugar"],
            sold_out_last=r["sold_out_last"],
            number_dispensed=r["number_dispensed"],
            price=r["price"],
            product_index=r["product_index"],
            product_identifier=r["product_identifier"],
            localized_name=r["localized_name"],
        )
        for r in rows
    ]


def ensure_product_names(conn, names):
    cur = conn.cursor()
    rows = [(n,) for n in names]
    query = f"INSERT OR IGNORE INTO {PRODUCT_TABLE} (name) VALUES (?)"
    cur.executemany(query, rows)
    conn.commit()


def update_product_from_product(conn, p: Product):
    cur = conn.cursor()
    query = f"""UPDATE {PRODUCT_TABLE} SET
      sold_out_last = ?,
      number_dispensed = ?,
      price = ?,
      product_index = ?,
      product_identifier = ?
    WHERE
      localized_name = ?
    """
    cur.execute(
        query,
        (
            p.sold_out_last,
            p.number_dispensed,
            p.price,
            p.product_index,
            p.product_identifier,
            p.localized_name,
        ),
    )


def update_products_from_products(conn, products):
    cur = conn.cursor()
    query = f"SELECT localized_name FROM {PRODUCT_TABLE}"
    cur.execute(query)
    existing_product_names = [r["localized_name"] for r in cur.fetchall()]
    for p in products:
        if p.localized_name in existing_product_names:
            # Perform update
            update_product_from_product(conn, p)
        else:
            print(f'Missing a localized_name for the value "{p.localized_name}"')
    conn.commit()


def insert_fill_event(conn, e: FillEvent):
    cur = conn.cursor()
    query = f"INSERT OR IGNORE INTO {FILL_EVENT_TABLE} (fill_date, insert_date, ingredient, value) VALUES (?, ?, ?, ?)"
    cur.execute(query, (e.fill_date, e.insert_date, e.ingredient, e.value))
    conn.commit()


def update_ingredient_level(conn, ilevel: IngredientLevel):
    cur = conn.cursor()
    query = f"INSERT OR IGNORE INTO {INGREDIENT_LEVEL_TABLE} (level_date, insert_date, ingredient, value) VALUES (?, ?, ?, ?)"
    cur.execute(query, (ilevel.level_date, ilevel.insert_date, ilevel.ingredient, ilevel.value))
    conn.commit()


def update_machine_numbers(conn, m: DispenserInfo):
    cur = conn.cursor()
    query = f"""UPDATE {DISPENSER_INFO_TABLE} SET
        last_cleaned = ?,
        initialization_date = ?,
        total_prod_dispensed = ?,
        coffee_beans_dispensed = ?,
        milk_dispensed = ?,
        choco_dispensed = ?,
        sugar_dispensed = ?
    """
    cur.execute(
        query,
        (
            m.last_cleaned,
            m.initialization_date,
            m.total_prod_dispensed,
            m.coffee_beans_dispensed,
            m.milk_dispensed,
            m.choco_dispensed,
            m.sugar_dispensed,
        ),
    )
    conn.commit()


def add_sqlite_latency(text):
    # Parses 2021-10-11 16:22:34.821000
    orignal_dt = datetime.strptime(text, "%Y-%m-%d %H:%M:%S.%f")
    # Adds 2 seconds to the timestamp
    new_dt = orignal_dt + timedelta(seconds=2)
    return new_dt.strftime("%Y-%m-%d %H:%M:%S.%f")


def update_ingredient_estimate(conn, fill, filldate, ingredient_name):
    cost_columns = {
        "Coffee Beans": "cost_coffee_beans",
        "Milk product": "cost_milk",
        "Chocolate": "cost_choco",
        "Sugar": "cost_sugar",
    }

    if ingredient_name not in cost_columns:
        print(f"Unknown column name in estimate_columns: {ingredient_name}")
        return

    cost_column = cost_columns[ingredient_name]
    cur = conn.cursor()

    remove_query = f"SELECT ROUND(SUM({cost_column}), 2) as cost FROM {DISPENSED_EVENT_TABLE} WHERE insert_date >= ?"
    cur.execute(remove_query, (filldate,))
    # print(filldate)
    cost = cur.fetchone()["cost"]
    if cost is None:
        cost = 0

    # Use datetime + 2 seconds because it should ignore the fill event right after the filldate
    new_dt = add_sqlite_latency(filldate)
    add_query = f'SELECT SUM(value) as "add" FROM {FILL_EVENT_TABLE} WHERE insert_date >= ? AND ingredient = ?'
    cur.execute(add_query, (new_dt, ingredient_name))
    add = cur.fetchone()["add"]
    if add is None:
        add = 0

    new_value = Decimal(fill) + Decimal(add) - Decimal(cost)
    # print(f"Update estimates! {new_value=}, {fill=}, {add=}, {cost=}")
    if new_value < 0:
        new_value = 0
    new_value = str(new_value)
    update_estimate_query = f"UPDATE {INGREDIENT_ESTIMATE_TABLE} SET estimate_fill_level = ? WHERE ingredient = ?"
    cur.execute(update_estimate_query, (new_value, ingredient_name))
    conn.commit()


def update_ingredient_estimates(conn):
    cur = conn.cursor()
    query = f"""SELECT ingredient,
          insert_date,
           value
    FROM {INGREDIENT_LEVEL_TABLE}
    WHERE id IN
        (SELECT max(id)
         FROM {INGREDIENT_LEVEL_TABLE}
         GROUP BY ingredient);
    """
    cur.execute(query)
    fill_levels = cur.fetchall()
    cur.close()
    for fill_level in fill_levels:
        ingredient = fill_level[0]
        insert_date = fill_level[1]
        value = fill_level[2]
        update_ingredient_estimate(conn, fill=value, filldate=insert_date, ingredient_name=ingredient)
