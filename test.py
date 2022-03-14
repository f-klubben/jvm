from mail_handler import handle_mail, update_statistics
from os import listdir
from os.path import join, isfile
from pathlib import Path
from generator import generate
from sqlite import get_sqlite_database
import sqlite3


CURR_DIR = Path(__file__).parent.resolve()
DIR = CURR_DIR / "test_mails"
DB_FILE = get_sqlite_database()


def ingest_emails():
    files = [str(join(DIR, f)) for f in listdir(DIR) if f.endswith(".eml") and isfile(join(DIR, f))]

    for f in sorted(files):
        with open(f, mode="r", encoding="utf-8") as e:
            handled, subject = handle_mail(e.read())
            if handled:
                # print(f'SUCCESS: correctly parse file: "{f}"')
                pass
            else:
                print(f'FAILURE: failed to parse file: "{f}"')
                print(f'Subject: "{subject}"')


def correct_database_timestamps():
    con = sqlite3.connect(str(DB_FILE))
    cur = con.cursor()
    test_migration = CURR_DIR / "migrations" / "99_fix_test_db.sql"
    with open(test_migration) as f:
        cur.executescript(f.read())


def final_step():
    update_statistics()
    generate.generate_coffee_report(DB_FILE)


def main():
    ingest_emails()
    correct_database_timestamps()
    final_step()


if __name__ == "__main__":
    main()
