from dotenv import load_dotenv

load_dotenv()
import asyncio

import pydash as _

from function.calc_points import select_label


def __init__():
    import config.database as db

    db.init()
    asyncio.run(select_label())


if __name__ == "__main__":
    __init__()
