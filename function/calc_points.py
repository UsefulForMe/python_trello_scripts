import asyncio
import copy
from datetime import datetime
import math

import aiohttp
import api.trello as trello
from modules.card.card_model import Card
import nest_asyncio
import pydash as _
from DateTime import DateTime
import re
import function.pandas as pd
import function.sheet as sheet
import modules.user.user_service as user_service
import modules.card.card_service as card_service

nest_asyncio.apply()

boards = trello.get_boards()
tech_board = _.find(boards, {"name": "Team Tech"})
board_id = tech_board.get("id")

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


def process_cards(cards):
    summary_cards = []
    cards_with_point = asyncio.run(get_points(cards))
    for card in cards_with_point:
        name_list_of_card = dict["lists"][card.get("idList")].get("name")
        if re.sub(r"[^a-zA-Z]+", "", name_list_of_card) not in [
            "Todo",
            "Doing",
            "Edit",
            "QC",
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
            "point": card["point"],
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
                clone_useful_info["point"] = math.ceil(
                    float(card["point"]) / len(available_members)
                )
                summary_cards.append(clone_useful_info)
    return summary_cards


def fill_sheet(data, columns):
    worksheet_data = []

    for card in data:
        row = [
            card.get("full_name", "Chưa có"),
            card["name"],
            card["labels"],
            card["point"],
            card["list"],
            card["short_url"],
            card["due_date"],
        ]
        worksheet_data.append(row)
    df = pd.create_dataframe(columns=columns, data=worksheet_data)
    df["Point"] = df["Point"].astype(int)
    sh = sheet.open_spreadsheet(
        name=f"Summary Point {datetime.today().strftime('%Y-%m-%d')} {int(datetime.today().isocalendar()[1])}"
    )
    ws = sheet.open_worksheet(sh, "Summary Point")
    sheet.fill_data(ws, dataframe=df)

    print("Done")
    sheet.share_with_many(sh, users=user_service.get_all_users())

    done_cards = _.map_(
        _.filter_(data, lambda card: card["list"] == "Done"),
        lambda card: Card.from_json(card),
    )

    card_service.insert_cards_in_week(done_cards)


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

    cards_in_label = _.filter_(cards, lambda card: id_label in card.get("idLabels"))
    processed_cards = process_cards(cards_in_label)
    return processed_cards


async def select_label():
    async with aiohttp.ClientSession() as session:
        labels = await trello.get_labels(board_id=board_id, session=session)
        labels.sort(key=sort_label)

        for index, label in enumerate(labels):
            print(f"{index}. {label.get('name')}")

        print("Chọn index label cần tính toán: ")
        index = int(input())
        if index < 0 or index > len(labels) - 1:
            raise "Vui lòng chọn index hợp lệ"
        choose_label = labels[index]
        cards = await calc(choose_label.get("id"))
        fields = [
            "Username",
            "Card Title",
            "Label",
            "Point",
            "Status",
            "Link",
            "Due Date",
        ]

        fill_sheet(cards, fields)
