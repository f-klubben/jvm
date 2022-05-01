import configparser
import logging

CONFIG = None


def read_config():
    global CONFIG
    if CONFIG is None:
        CONFIG = configparser.ConfigParser()
        CONFIG.read("config.ini")


def get_server_settings():
    read_config()
    ip = CONFIG.get("default", "ip", fallback="0.0.0.0")
    port = CONFIG.getint("default", "port", fallback=2525)
    capture = CONFIG.get("default", "capture", fallback="ALL")
    if capture not in ["ALL", "UNPARSED", "NONE"]:
        logging.error(f'Unknown value in the config file for capture: "{capture}"')
    return {"ip": ip, "port": port, "capture": capture}


def get_notif_settings():
    read_config()
    return {
        "debug": CONFIG.get("slack", "debug", fallback=True),
        "slack_token": CONFIG.get("slack", "token", fallback=""),
        "channel_id": CONFIG.get("slack", "channel_id", fallback=""),
        "threshold_percentage": CONFIG.get("slack", "threshold_percentage", fallback=0.25),
        "notif_data_path": CONFIG.get("slack", "notif_data_path", fallback=""),
    }


def setup_logging():
    read_config()
    loglevel = CONFIG.get("log", "level", fallback="DEBUG")
    logfile = CONFIG.get("log", "filename", fallback=None)

    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"Invalid log level: {loglevel}")
    logging.basicConfig(
        filename=logfile,
        level=numeric_level,
        format="[%(asctime)s] [%(funcName)s:%(lineno)d] %(message)s",
    )


def get_db_file():
    read_config()
    return CONFIG.get("database", "location", fallback="db.sqlite3")


if __name__ == "__main__":
    setup_logging()
    logging.debug(f"get_server_settings()={get_server_settings()}")
    logging.debug(f"get_notif_settings()={get_notif_settings()}")
    logging.debug(f"get_db_file()='{get_db_file()}'")
