import pickle
import sqlite3
import datetime
from pathlib import Path

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import get_notif_settings

from generator.generate import INGREDIENT_ESTIMATE

DEBUG = True
SETTINGS = get_notif_settings()
THRESHOLD_PERCENTAGE = float(SETTINGS["threshold_percentage"])
CHANNEL_ID = SETTINGS["channel_id"]
NOTIF_DATA_PATH = SETTINGS["notif_data_path"]
CLIENT = WebClient(token=SETTINGS["slack_token"])


def get_notif_last_data():
    try:
        with open(NOTIF_DATA_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        data = {
            "Kaffebønner": datetime.datetime.now() - datetime.timedelta(days=1, hours=1),
            "Chokolade": datetime.datetime.now() - datetime.timedelta(days=1, hours=1),
            "Mælkeprodukt": datetime.datetime.now() - datetime.timedelta(days=1, hours=1),
            "Sukker": datetime.datetime.now() - datetime.timedelta(days=1, hours=1),
        }
        write_notif_data(data)
        return data


def write_notif_data(data: dict):
    try:
        with open(NOTIF_DATA_PATH, "wb") as f:
            pickle.dump(data, f)
    except Exception as e:
        print("Could not dump last notif data:", e)


def send_slack_msg(msg: str, thread_ts: str = None) -> bool:
    if DEBUG:
        print(msg, thread_ts)
        return True
    try:
        result = CLIENT.chat_postMessage(channel=CHANNEL_ID, thread_ts=thread_ts, text=msg)
        # if message succeeded, return ts of the message which is required for replying in future
        if result["ok"]:
            return result["ts"]
        else:
            return False

    except SlackApiError as e:
        print(f"Error sending message to {CHANNEL_ID}: {e}")


def under_threshold_ingredients():
    cur = sqlite3.connect(str(Path(__file__ + "/../db.sqlite3").resolve())).cursor()
    cur.execute(INGREDIENT_ESTIMATE)
    return cur.fetchall()


def handle_low_level():
    ingredients = under_threshold_ingredients()
    last_notif = get_notif_last_data()
    for i, s, c, m in ingredients:
        threshold = m * THRESHOLD_PERCENTAGE
        # check if this threshold has not been notified within the past day, and is triggered
        if c < threshold and last_notif[s] < datetime.datetime.now() - datetime.timedelta(days=1):
            send_slack_msg(f"{s} needs to be refilled! Threshold: {threshold}, but {s} at {c}/{m})")
            # update last notif data
            last_notif[s] = datetime.datetime.now()
    # write any updated notif data
    write_notif_data(last_notif)


handle_low_level()
