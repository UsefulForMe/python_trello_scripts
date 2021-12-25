import datetime as DateTime


class Card:
    def __init__(
        self,
        id,
        name,
        desc,
        id_board,
        id_member,
        labels=None,
        short_url=None,
        point=None,
    ):
        self.id = id
        self.name = name
        self.desc = desc
        self.id_board = id_board
        self.id_member = id_member
        self.labels = labels
        self.short_url = short_url
        self.point = point

    @staticmethod
    def from_tuple(tuple):
        return Card(*tuple)

    @staticmethod
    def from_json(json):
        return Card(
            json["id"],
            json["name"],
            json["desc"],
            json["id_board"],
            json["id_member"] if "id_member" in json else "",
            json["labels"],
            json["short_url"],
            json["point"] if "point" in json else 0,
        )

    def to_tuple(self):
        return (
            self.id + "-" + self.id_member,
            self.name,
            self.desc,
            self.id_board,
            self.id_member,
            self.labels,
            self.short_url,
            self.point,
            int(DateTime.date.today().isocalendar()[1]),
        )


sql_create_card_table = """ CREATE TABLE IF NOT EXISTS cards (
                                        id text PRIMARY KEY,
                                        name text NOT NULL,
                                        desc text,
                                        id_board text NOT NULL,
                                        id_member text, 
                                        labels text,
                                        short_url text,
                                        point real,
                                        week integer,
                                        FOREIGN KEY(id_member) REFERENCES users(id)
                                    ); """
