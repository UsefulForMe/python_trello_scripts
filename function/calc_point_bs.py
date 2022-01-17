import asyncio
import copy
import math
import re
from datetime import datetime

import aiohttp
import api.trello as trello
import modules.card.card_service as card_service
import modules.user.user_service as user_service
import nest_asyncio
import pydash as _
from DateTime import DateTime
from modules.card.card_model import Card
from platformdirs import os

import function.pandas as pd
import function.sheet as sheet

nest_asyncio.apply()

boards = trello.get_boards()

board_name= os.environ.get("TRELLO_BOARD_NAME")
board = _.find(boards, {"name": board_name})
board_id = board.get("id")

switcher = {0: "members", 1: "custom_fields", 2: "lists", 3: "labels"}
dict = {"members": {}, "custom_fields": {}, "lists": {}, "labels": {}}


def sort_label(label):
    name = label.get("name")
    if "/" not in name:
        return "0"
    name_split = name.split("/")
    name_split.reverse()
    return "/".join(name_split)


def make_dict(data, index):
    key = switcher[index]
    if key is not None:
        for item in data:
            dict[key][item.get("id")] = item


async def get_points(cards):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for card in cards:
            tasks.append(asyncio.create_task(get_point(card, session)))
        cards_with_point = await asyncio.gather(*tasks, return_exceptions=True)
        return cards_with_point


async def get_point(card, session):
    point = await trello.get_point(card, session)
    card["point"] = point
    return card




def process_cards_bs(cards):
    summary_cards = []
    
    for card in cards:
        name_list_of_card = dict["lists"][card.get("idList")].get("name")
        if re.sub(r"[^a-zA-Z]+", "", name_list_of_card) not in [
            "Backlog",
            "Todo",
            "Doing",
            "Done",
        ]:
            continue

        dueDate = dueDate = DateTime(card["due"]).Date() if card["due"] else ""
        useful_info = {
            "id": card["id"],
            "name": card["name"],
            "desc": card["desc"],
            "id_board": card["idBoard"],
            "labels": ", ".join(
                [dict["labels"][id_label]["name"] for id_label in card["idLabels"]]
            ),
            "short_url": card["shortUrl"],
            "list": re.sub(r"[^a-zA-Z]+", "", name_list_of_card),
            "due_date": dueDate,
        }
        if not len(card["idMembers"]):
            summary_cards.append(useful_info)
        else:
            # get available members
            available_members = _.filter_(
                card["idMembers"], lambda member: member in dict["members"]
            )

            for member in available_members:
                clone_useful_info = copy.deepcopy(useful_info)
                clone_useful_info["username"] = dict["members"][member]["fullName"]
                clone_useful_info["full_name"] = dict["members"][member]["fullName"]
                clone_useful_info["id_member"] = dict["members"][member]["id"]
                summary_cards.append(clone_useful_info)
    return summary_cards




def fill_sheet_bs(data, columns):
    worksheet_data = []

    for card in data:
        row = [
            card.get("full_name", "Chưa có"),
            card["name"],
            card["labels"],
            card["list"],
            card["short_url"],
            card["due_date"],
        ]
        worksheet_data.append(row)
    df = pd.create_dataframe(columns=columns, data=worksheet_data)
    sh = sheet.open_spreadsheet(
        name=f"Summary Card {datetime.today().strftime('%Y-%m-%d')} {int(datetime.today().isocalendar()[1])}"
    )
    ws = sheet.open_worksheet(sh, "Summary Card")
    sheet.fill_data(ws, dataframe=df)

    print("Done")


async def calc(id_label):
    async with aiohttp.ClientSession() as session:
        data = await asyncio.gather(
            *[
                asyncio.create_task(
                    trello.get_members(board_id=board_id, session=session)
                ),
                trello.get_custom_fields(board_id=board_id, session=session),
                trello.get_lists(board_id=board_id, session=session),
                trello.get_labels(board_id=board_id, session=session),
                trello.get_cards(board_id=board_id, session=session),
            ]
        )

    for index, _data in enumerate(data[0:4]):
        make_dict(_data, index)

    cards = data[4]
    if(id_label):
        cards = _.filter_(cards, lambda card: id_label in card["idLabels"])

    processed_cards = process_cards_bs(cards)
    return processed_cards



async def summarize_card():
    async with aiohttp.ClientSession() as session:
        cards = await calc(None)
        fields = [
            "Username",
            "Card Title",
            "Label",
            "Status",
            "Link",
            "Due Date",
        ]

        fill_sheet_bs(cards, fields)
