import pickle
import sqlite3
from datetime import datetime
from datetime import timedelta
from pathlib import Path

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import get_notif_settings

from generator.generate import INGREDIENT_ESTIMATE

SETTINGS = get_notif_settings()
DEBUG = False if SETTINGS["debug"] == "false" else True
THRESHOLD_PERCENTAGE = float(SETTINGS["threshold_percentage"])
CHANNEL_ID = SETTINGS["channel_id"]
NOTIF_DATA_PATH = SETTINGS["notif_data_path"]
DEFAULT_LAST_NOTIF_TIME = datetime.now() - timedelta(days=1, hours=1)
CLIENT = WebClient(token=SETTINGS["slack_token"])


# class holding last update, last notification, and resolve status as args TODO update
class NotifData:
    def __init__(self, last_notif=None, last_notif_ts=None):
        self.last_notif: datetime = last_notif
        self.last_notif_ts: str = last_notif_ts


def get_notif_last_data():
    try:
        with open(NOTIF_DATA_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # init notif data if it does not exist
        data = {
            "Kaffebønner": NotifData(),
            "Chokolade": NotifData(),
            "Mælkeprodukt": NotifData(),
            "Sukker": NotifData(),
        }
        write_notif_data(data)
        return data


def write_notif_data(data: dict):
    try:
        with open(NOTIF_DATA_PATH, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        print("Could not dump last notif data:", e)


def send_slack_msg(msg: str, thread_ts: str = None) -> str | None:
    if DEBUG:
        print(msg, thread_ts)
        return "42.69"
    try:
        # react with fixd and remove warning if resolved
        if thread_ts:
            CLIENT.reactions_remove(channel=CHANNEL_ID, timestamp=thread_ts,  name="warning")
            CLIENT.reactions_add(channel=CHANNEL_ID, timestamp=thread_ts, name="fixd")

        result = CLIENT.chat_postMessage(channel=CHANNEL_ID, thread_ts=thread_ts, text=msg)
        # if message succeeded, return ts of the message which is required for replying in future
        if result["ok"]:
            # react with warning to highlight active low levels
            CLIENT.reactions_add(channel=CHANNEL_ID, timestamp=result["ts"], name="warning")
            return result["ts"]
        else:
            return None

    except SlackApiError as e:
        print(f"Error sending message to {CHANNEL_ID}: {e}")


def ingredient_levels():
    cur = sqlite3.connect(str(Path(__file__ + "/../db.sqlite3").resolve())).cursor()
    cur.execute(INGREDIENT_ESTIMATE)
    return cur.fetchall()


def notify_on_low_ingredient_levels():
    # get curr ingredients and last notif data
    ingredients = ingredient_levels()
    notif_data = get_notif_last_data()

    for _, s, c, m in ingredients:
        threshold = m * THRESHOLD_PERCENTAGE

        if c <= threshold:
            # if not notified
            if not notif_data[s].last_notif:
                # send message
                res = send_slack_msg(
                    f"@channel ACTION NEEDED! {s} needs to be refilled. Threshold: {threshold}, but {c}/{m} grams left"
                )
                if res:
                    # update last notif data if msg was sent successfully
                    notif_data[s].last_notif = datetime.now()
                    notif_data[s].last_notif_ts = res
                else:
                    print(f"Could not send notif message for {s}, will not update last notif data")

        # above threshold, check if notif sent with 12 hours
        else:
            if notif_data[s].last_notif and notif_data[s].last_notif > datetime.now() - timedelta(hours=12):
                # send resolve message
                res = send_slack_msg(
                    f"RESOLVED! {s} is above threshold again. "
                    f"Resolved within {datetime.now() - notif_data[s].last_notif}",
                    notif_data[s].last_notif_ts,
                )
                if res:
                    # reset notif data if msg was sent successfully
                    notif_data[s] = NotifData()
                else:
                    print(f"Could not send resolve message for {s}, retrying next run")

    # write updated notif data
    write_notif_data(notif_data)


notify_on_low_ingredient_levels()
