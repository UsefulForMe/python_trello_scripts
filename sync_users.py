import json

from dotenv import load_dotenv

load_dotenv()

import pydash as _

import config.database as db
from modules.user.user_model import User
from modules.user.user_service import get_all_users, insert_users, remove_all_users

db.init()

# Opening JSON file
f = open(
    "data/users.json",
)

data = json.load(f)


users = _.map_(
    data,
    lambda user: User.from_json(user),
)
remove_all_users()
insert_users(users)
users = get_all_users()

for user in users:
    print(user.to_json())
