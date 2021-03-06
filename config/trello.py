import os

TRELLO_USER_ID = os.environ.get("TRELLO_USER_ID")
TRELL_ACCESS_TOKEN = os.environ.get("TRELL_ACCESS_TOKEN")
TRELLO_KEY = os.environ.get("TRELLO_KEY")

trello = {
    "USER_ID": TRELLO_USER_ID,
    "ACCESS_TOKEN_TRELLO": TRELL_ACCESS_TOKEN,
    "KEY": TRELLO_KEY,
}
