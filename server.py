from __future__ import print_function
from datetime import datetime

import notifier
from mail_handler import handle_mail, update_statistics
import asyncore
from smtpd import SMTPServer
import os
from datetime import datetime
from config import get_server_settings, setup_logging
from sqlite import get_sqlite_database
from generator import generate
import logging

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
    logging.warning(f"{filename} saved.")


class KaffeLogger(SMTPServer):
    no = 0
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
        try:
            handled, _ = handle_mail(text)
        except:
            logging.exception("Unable to parse email")
        if self.capture == "ALL" or ((not handled) and self.capture == "UNPARSED"):
            save_email(text, self.no)
            self.no += 1
        update_statistics()
        generate.generate_coffee_report(get_sqlite_database())
        notifier.notify_on_low_ingredient_levels()


def run():
    # start the smtp server on 0.0.0.0:1025
    ip = CONFIG["ip"]
    port = CONFIG["port"]
    capture = CONFIG["capture"]
    KaffeLogger((ip, port), None)
    logging.info(f"Now listening for mails on ip: {ip}, port {port}")
    logging.info(f"Capturing emails: {capture}")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    setup_logging()
    run()
