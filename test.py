from mail_handler import handle_mail, update_statistics
from os import listdir
from os.path import join, isfile
from pathlib import Path
from generator import generate
import sqlite3

DIR = "test_mails"

CURR_DIR = Path(__file__).parent.resolve()
DB_FILE = CURR_DIR / "db.sqlite3"

files = [str(join(DIR, f)) for f in listdir(DIR) if f.endswith(".eml") and isfile(join(DIR, f))]


for f in sorted(files):
    with open(f, "r") as e:
        handled, subject = handle_mail(e.read())
        if handled:
            # print(f'SUCCESS: correctly parse file: "{f}"')
            pass
        else:
            print(f'FAILURE: failed to parse file: "{f}"')
            print(f'Subject: "{subject}"')

con = sqlite3.connect(DB_FILE)
cur = con.cursor()
test_migration = CURR_DIR / "migrations/99_fix_test_db.sql"
with open(test_migration) as f:
    cur.executescript(f.read())

update_statistics()
generate.generate_coffee_report(DB_FILE)
