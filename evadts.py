from models import Product
from datetime import datetime


def parse_evadts_date(text):
    # 211006*122610
    return datetime.strptime(text, "%y%m%d*%H%M%S")


def parse_custom_evadts_date(text):
    # 20211006*122610
    return datetime.strptime(text, "%Y%m%d*%H%M%S")


def split_evadts_str(line):
    return line.split("*")


# Parses a line like this:
# ID5*991215*000001**OFF
def parse_id5_tag(line):
    return parse_evadts_date(line[4:17])


def parse_product_info(lines):
    pa1_split = split_evadts_str(lines[0])
    pa4_split = split_evadts_str(lines[3])
    last_sold_out_date = parse_evadts_date(lines[4][4:])
    pa6_split = split_evadts_str(lines[5])
    return Product(
        id=None,
        name=None,
        cost_coffee_beans=None,
        cost_milk=None,
        cost_choco=None,
        cost_sugar=None,
        sold_out_last=last_sold_out_date,
        number_dispensed=pa4_split[1],
        price=pa4_split[2],
        product_index=pa1_split[1],
        product_identifier=pa6_split[1],
        localized_name=pa1_split[3],
    )


def parse_machine_last_cleaned(line):
    split = split_evadts_str(line)
    if split[1] != "LAST CLEANED":
        return None
    return parse_custom_evadts_date(line[17:])


def parse_machine_init(line):
    return parse_custom_evadts_date(line[4:])


def parse_ingredient_dispensed(line):
    split = split_evadts_str(line)
    return (split[1], int(split[3]))


def parse_free_vends(line):
    split = split_evadts_str(line)
    return int(split[2])
