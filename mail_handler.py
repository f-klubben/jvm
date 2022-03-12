import re
import base64
from datetime import datetime
from models import DispensedEvent, FillEvent, DispenserInfo, IngredientLevel
from sqlite import (
    create_db_conn,
    ensure_product_names,
    get_products,
    insert_dispensed_drink_event,
    update_products_from_products,
    insert_fill_event,
    update_ingredient_level,
    update_machine_numbers,
    update_ingredient_estimates,
)
from util import parse_email_date
from evadts import (
    parse_product_info,
    parse_machine_last_cleaned,
    parse_machine_init,
    parse_ingredient_dispensed,
    parse_free_vends,
)

# Handles the "DispensedDrinkEvent"
# Each mail contains the 10 last DispensedDrinkEvent
def handle_dispensed(mail):
    # Parses a string like this:
    # 06/10/2021 08:47:43:177  DispensedDrinkEvent  "Filter coffee" "succes"
    matches = re.findall(
        r"(\d+\/\d+\/\d+\s\d+:\d+:\d+:\d+)\s+DispensedDrinkEvent\s+\"(.+?)\"\s+\"(.+?)\"",
        mail,
    )
    if len(matches) == 0:
        return
    product_names = [m[1] for m in matches]
    conn = create_db_conn()
    ensure_product_names(conn, product_names)
    products = get_products(conn)
    product_dict = {p.name: p for p in products}
    for m in matches:
        dispensed_date = parse_email_date(m[0])
        dispensed_product = product_dict[m[1]]
        dispensed_status = m[2]
        insert_date = datetime.now()
        e = DispensedEvent(dispensed_date, dispensed_status, insert_date)
        insert_dispensed_drink_event(conn, e, dispensed_product)


def handle_status(mail):
    mail_index = mail.find("Content-disposition: attachment")
    attach = mail[mail_index:].splitlines()
    base64_str = "".join(attach[2:-2])
    message_bytes = base64.b64decode(base64_str)
    message = message_bytes.decode("utf-8")
    lines = message.splitlines()
    d = DispenserInfo()
    products = []
    for i in range(len(lines)):
        if lines[i].startswith("PA1"):
            products.append(parse_product_info(lines[i : i + 6]))
        if lines[i].startswith("MA5"):
            machine_config = parse_machine_last_cleaned(lines[i])
            if machine_config is None:
                continue
            d.last_cleaned = machine_config
        if lines[i].startswith("EA4"):
            d.initialization_date = parse_machine_init(lines[i])
        if lines[i].startswith("SA2"):
            res = parse_ingredient_dispensed(lines[i])
            if res[0] == "Coffee Beans":
                d.coffee_beans_dispensed = res[1]
            elif res[0] == "Milk product":
                d.milk_dispensed = res[1]
            elif res[0] == "Sugar":
                d.choco_dispensed = res[1]
            elif res[0] == "Chocolate":
                d.sugar_dispensed = res[1]
            else:
                print(f'Unknown ingredient "{res[0]}"')
        if lines[i].startswith("VA3"):
            d.total_prod_dispensed = parse_free_vends(lines[i])
    if len(products) == 0:
        return
    conn = create_db_conn()
    update_products_from_products(conn, products)
    update_machine_numbers(conn, d)


def handle_ingredient_change(mail):
    # Parses a string like this:
    # 09/03/2020 10:33:15:727  IngredientLevel  "Ingredient 'Sugar' is filled." Current grams: 2400
    matches = re.findall(r"(\d+\/\d+\/\d+\s\d+:\d+:\d+:\d+)\s+IngredientLevel\s+\"(.*?)\"\s(.*)", mail)
    if len(matches) == 0:
        return
    conn = create_db_conn()
    for m in matches:
        msg_res = re.match(r"Ingredient\s'(.*?)' is", m[1])
        if not msg_res:
            continue
        ingredient = msg_res[1]
        ingredient_date = parse_email_date(m[0])
        ingredient_fill_level = re.match(r"Current grams: (\d+)", m[2])[1]
        insert_date = datetime.now()
        ilvl: IngredientLevel = IngredientLevel(
            level_date=ingredient_date,
            insert_date=insert_date,
            ingredient=ingredient,
            value=ingredient_fill_level,
        )
        update_ingredient_level(conn, ilvl)


def handle_menu_param(mail):
    matches = re.findall(r'(\d+\/\d+\/\d+\s\d+:\d+:\d+:\d+)\s+Menu parametre\s+"(.*?)"', mail)
    if len(matches) == 0:
        return
    conn = create_db_conn()
    for m in matches:
        event_date = parse_email_date(m[0])
        event_msg = m[1]
        # Tøm beholder-500grCoffee Beans
        r = re.match(r"(.*?)([+-]\d+)gr(.*)", event_msg)
        if not r:
            continue

        if r[1] in ["Fylde beholder", "Tøm beholder"]:
            insert_date = datetime.now()
            e = FillEvent(
                fill_date=event_date,
                insert_date=insert_date,
                ingredient=r[3],
                value=int(r[2]),
            )
            insert_fill_event(conn, e)


def update_statistics():
    conn = create_db_conn()
    update_ingredient_estimates(conn)


def handle_mail(mail) -> bool:
    subject = None

    IGNORE_SUBJECTS = (
        "ApplicationStartEvent",
        "CleaningEvent",
        "CPUFanEvent",
        "Drip Tray not present",
        "Drypbakke fuld",
        "Drypbakke mangler",
        "Empty Doser Chocolate",
        "Fejl på pisker 1",
        "Fejl på pisker 2",
        "Maskinkort",
        "Menu adgang",
        "Rengørrings begivenhed",
        "Solid waste full",
        "TEST",
        "Utlevere Drikk Hendelser",
        "WasteLevel",
    )

    subject_match = re.search("Subject: (.*)", mail)
    if subject_match:
        subject = subject_match.group(1)

    if not subject:
        return (False, None)

    if subject.endswith("DispensedDrinkEvent"):
        handle_dispensed(mail)
    elif subject.endswith("EVADTS status"):
        handle_status(mail)
    elif subject.endswith("IngredientLevel"):
        handle_ingredient_change(mail)
    elif subject.endswith("Menu parametre") or subject.endswith("MenuParameter"):
        handle_menu_param(mail)
    elif subject.endswith(IGNORE_SUBJECTS):
        # Ignore
        pass
    else:
        return (False, subject)

    return (True, None)
