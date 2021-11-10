import requests
import pydash as _
from config.trello import trello

headers = {"Accept": "application/json"}
query = {
    "token": f'{trello["ACCESS_TOKEN_TRELLO"]}',
    "key": f'{trello["KEY"]}',
}

BASE_URL = "https://api.trello.com/1"


def get_boards():
    try:
        response_boards = requests.request(
            "GET",
            f'{BASE_URL}/members/{trello["USER_ID"]}/boards',
            params=query,
            headers=headers,
        )

        boards = response_boards.json()
        return boards
    except Exception:
        raise Exception


async def get_lists(board_id: str, session):
    try:
        url = f"{BASE_URL}/boards/{board_id}/lists"
        async with session.get(
            url,
            headers=headers,
            params=query,
        ) as response:
            json = await response.json()
            return json
    except Exception:
        raise Exception


async def get_labels(board_id: str, session):
    try:
        url = f"{BASE_URL}/boards/{board_id}/labels"
        async with session.get(
            url,
            headers=headers,
            params=query,
        ) as response:
            json = await response.json()
            return json
    except Exception:
        raise Exception


async def get_members(board_id: str, session):
    try:
        url = f"{BASE_URL}/boards/{board_id}/members"
        async with session.get(
            url,
            headers=headers,
            params=query,
        ) as response:
            json = await response.json()
            return json
    except Exception:
        raise Exception


async def get_custom_fields(board_id: str, session):
    try:
        url = f"{BASE_URL}/boards/{board_id}/customFields"
        async with session.get(
            url,
            headers=headers,
            params=query,
        ) as response:
            json = await response.json()
            return json
    except Exception:
        raise Exception


async def get_cards(board_id: str, session):
    try:
        url = f"{BASE_URL}/boards/{board_id}/cards"
        async with session.get(
            url,
            headers=headers,
            params=query,
        ) as response:
            json = await response.json()
            return json
    except Exception:
        raise Exception


async def get_point(card, session):
    try:
        url = f'{BASE_URL}/cards/{card.get("id")}/customFieldItems'

        async with session.get(
            url,
            headers=headers,
            params=query,
        ) as response:
            point = 0
            if response.status != 200:
                return 0

            response = await response.json()
            custom_field = _.find(
                response, {"idCustomField": "5f8e5b92e141341c11fe1b1d"}
            )
            if custom_field:
                point = custom_field["value"]["number"]
            return point

    except Exception:
        raise Exception
