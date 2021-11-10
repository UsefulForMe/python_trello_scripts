from modules.card.card_model import Card
from config.database import create_connection
import pydash as _
import datetime as DateTime

conn = create_connection()
cur = conn.cursor()


def insert_cards(body: list["Card"]):
    cards = []
    for card in body:
        id_members = ", ".join(card.id_members)
        id_labels = ", ".join(card.labels)
        cards.append(
            (
                card.id,
                card.name,
                card.desc,
                card.id_board,
                id_members,
                id_labels,
                card.short_url,
                card.id_list,
                card.point,
                str(DateTime.date.today().isocalendar()[1]),
            )
        )
    cur.executemany("insert into cards values (?, ?, ?, ?, ?, ? ,? ,? ,? ,?)", cards)
    conn.commit()
