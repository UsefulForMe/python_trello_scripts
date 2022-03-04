from os import environ
from dotenv import load_dotenv

load_dotenv()
import asyncio

import pydash as _

import function.calc_point_bs as bs
import function.calc_points as tech


def __init__():
    import config.database as db

    db.init()
    board_name = environ.get("TRELLO_BOARD_NAME")
    print(board_name)

    if board_name=='Business Solution':
        asyncio.run(bs.summarize_card())
    else:
        asyncio.run(tech.select_label())

if __name__ == "__main__":
    __init__()
