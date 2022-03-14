import configparser

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
        print(f'Unknown value in the config file for capture: "{capture}"')
    return {"ip": ip, "port": port, "capture": capture}


def get_db_file():
    read_config()
    return CONFIG.get("database", "location", fallback="db.sqlite3")


if __name__ == "__main__":
    print(f"get_server_settings()={get_server_settings()}")
    print(f"get_db_file()={get_db_file()}")
