import modules.user.user_model as user_model
from config.database import create_connection
import pydash as _

User = user_model.User

conn = create_connection()
cur = conn.cursor()


def insert_users(body: list["User"]):
    users = []
    for user in body:
        users.append(user.to_puple())
    cur.executemany("insert into users values (?, ?, ?, ?)", users)
    conn.commit()


def remove_all_users():
    cur.execute("delete from users")
    conn.commit()


def get_all_users():
    cur.execute("select * from users")
    users = _.map_(cur.fetchall(), lambda user: User.from_puple(user))
    return users
