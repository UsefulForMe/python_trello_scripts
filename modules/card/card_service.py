from modules.card.card_model import Card
from config.database import create_connection
import pydash as _
import datetime as DateTime

conn = create_connection()
cur = conn.cursor()


def insert_cards(body: list["Card"]):
    cards = []
    for card in body:
        cards.append(card.to_tuple())
    cur.executemany("insert into cards values (?, ?, ?, ?, ?, ? ,? ,? ,? )", cards)
    conn.commit()


def clear_card_in_week(week: int):
    cur.execute("delete from cards where week = ?", (week,))
    conn.commit()


def insert_cards_in_week(body: list["Card"]):
    clear_card_in_week(DateTime.date.today().isocalendar()[1])
    insert_cards(body)
