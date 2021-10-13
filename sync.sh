#!/usr/bin/env sh

echo "Copy database from remote to local"
rsync -azhP kaffelogger:/home/pi/code/jvm/db.sqlite3 ./remote.sqlite3 

echo "Copy mails from remote to local"
rsync -azhP -r kaffelogger:/home/pi/code/jvm/logged_mails/ ./test_mails

echo "Copy python files from local to remote"
rsync -azhP *.py kaffelogger:/home/pi/test/
rsync -azhP *.json kaffelogger:/home/pi/code/jvm/
