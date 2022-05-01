import pickle
import sqlite3
from datetime import datetime
from datetime import timedelta
from pathlib import Path

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import get_notif_settings

from sqlite import (
    create_db_conn,
    get_notifications,
    get_ingredient_estimates,
    update_notifications,
)

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

    def __repr__(self):
        return f"NotifData(last_notif={self.last_notif},last_notif_ts={self.last_notif_ts})"


def write_notif_data(data: dict):
    objs = [
        {
            "last_notif": datetime.strptime(v.last_notif, "%Y-%m-%d %H:%M:%S.%f"),
            "last_notif_ts": v.last_notif_ts,
            "ingredient": k,
        }
        for k, v in data.items()
    ]
    with create_db_conn() as conn:
        update_notifications(conn, objs)


def send_slack_msg(msg: str, thread_ts: str = None):
    if DEBUG:
        print(msg, thread_ts)
        return "42.69"
    try:
        # react with fixd and remove warning if resolved
        if thread_ts:
            CLIENT.reactions_remove(channel=CHANNEL_ID, timestamp=thread_ts, name="warning")
            CLIENT.reactions_add(channel=CHANNEL_ID, timestamp=thread_ts, name="fixd")

        result = CLIENT.chat_postMessage(channel=CHANNEL_ID, thread_ts=thread_ts, text=msg)
        # if message succeeded, return ts of the message which is required for replying in future
        if result["ok"]:
            # react with warning to highlight active low levels
            if not thread_ts:
                CLIENT.reactions_add(channel=CHANNEL_ID, timestamp=result["ts"], name="warning")
            return result["ts"]
        else:
            return None

    except SlackApiError as e:
        print(f"Error sending message to {CHANNEL_ID}: {e}")


def fetch_database_values():
    with create_db_conn() as conn:
        ingredient_estimates = get_ingredient_estimates(conn)
        notifications = get_notifications(conn)
        notif_datas = {}
        for _, ingredient, last_notif, last_notif_ts in notifications:
            if last_notif:
                last_notif = datetime.strptime(last_notif, "%Y-%m-%d %H:%M:%S.%f")
            notif_datas[ingredient] = NotifData(last_notif, last_notif_ts)
        return (ingredient_estimates, notif_datas)


def notify_on_low_ingredient_levels():
    # get curr ingredients and last notif data
    ingredients, notif_data = fetch_database_values()

    for _, ingredient, estimate_fill_level, max_level, localized_name in ingredients:
        threshold = max_level * THRESHOLD_PERCENTAGE

        current_notif = notif_data[ingredient]

        if estimate_fill_level <= threshold:
            # if not notified
            if not current_notif.last_notif:
                # send message
                res = send_slack_msg(
                    f"@channel ACTION NEEDED! {ingredient} needs to be refilled. Threshold: {threshold}, but {estimate_fill_level}/{max_level} grams left"
                )
                if res:
                    # update last notif data if msg was sent successfully
                    current_notif.last_notif = datetime.now()
                    current_notif.last_notif_ts = res
                    notif_data[ingredient] = current_notif
                else:
                    print(f"Could not send notif message for {ingredient}, will not update last notif data")

        # above threshold, check if notif sent
        else:
            if current_notif.last_notif:
                # send resolve message
                res = send_slack_msg(
                    f"RESOLVED! {ingredient} is above threshold again. "
                    f"Resolved within {datetime.now() - current_notif.last_notif}",
                    current_notif.last_notif_ts,
                )
                if res:
                    # reset notif data if msg was sent successfully
                    current_notif = NotifData()
                    notif_data[ingredient] = current_notif
                else:
                    print(f"Could not send resolve message for {ingredient}, retrying next run")

    # write updated notif data
    write_notif_data(notif_data)


if __name__ == "__main__":
    notify_on_low_ingredient_levels()
