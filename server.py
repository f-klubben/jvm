from __future__ import print_function
from datetime import datetime
from mail_handler import handle_mail, update_statistics
import asyncore
from smtpd import SMTPServer
import sys
import os
from datetime import datetime, timedelta
from config import get_server_settings
from sqlite import get_sqlite_database
from generator import generate

CONFIG = get_server_settings()


def save_email(text, no):
    capture_dir = "logged_mails"
    if not os.path.exists(capture_dir):
        os.mkdir(capture_dir)

    datestr = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{datestr}_{no}.eml"
    path = os.path.join(capture_dir, filename)
    with open(path, "w") as f:
        f.write(text)
    print(f"{filename} saved.")


class KaffeLogger(SMTPServer):
    no = 0
    last_update = datetime.now()
    capture = CONFIG["capture"].upper()

    def process_message(
        self,
        peer,
        mailfrom,
        rcpttos,
        data,
        mail_options=["BODY=8BITMIME", "SMTPUTF8"],
        rcpt_options=[],
    ):
        text = data.decode("UTF-8")
        handled, _ = handle_mail(text)
        if self.capture == "ALL" or ((not handled) and self.capture == "UNPARSED"):
            save_email(text, self.no)
            self.no += 1
            update_statistics()
            generate.generate_coffee_report(get_sqlite_database())
            self.last_update = datetime.now()


def run():
    # start the smtp server on 0.0.0.0:1025
    ip = CONFIG["ip"]
    port = CONFIG["port"]
    capture = CONFIG["capture"]
    foo = KaffeLogger((ip, port), None)
    print(f"Now listening for mails on ip: {ip}, port {port}")
    print(f"Capturing emails: {capture}")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    run()
