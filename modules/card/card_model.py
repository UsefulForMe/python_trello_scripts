class Card:
    def __init__(
        self,
        id,
        name,
        desc,
        id_board,
        id_members,
        labels=None,
        short_url=None,
        id_list=None,
        point=None,
    ):
        self.id = id
        self.name = name
        self.desc = desc
        self.id_board = id_board
        self.id_members = id_members
        self.labels = labels
        self.short_url = short_url
        self.id_list = id_list
        self.point = point

    @staticmethod
    def from_json(json):
        return Card(
            id=json["id"],
            name=json["name"],
            desc=json["desc"],
            id_board=json["idBoard"],
            id_members=json["idMembers"],
            labels=json["labels"],
            short_url=json["shortUrl"],
            id_list=json["idList"],
            point=json["pos"],
        )

    @staticmethod
    def to_json(card):
        return {
            "id": card.id,
            "name": card.name,
            "desc": card.desc,
            "idBoard": card.id_board,
            "idMembers": card.id_members,
            "labels": card.labels,
            "shortUrl": card.short_url,
            "idList": card.id_list,
            "pos": card.point,
        }


sql_create_card_table = """ CREATE TABLE IF NOT EXISTS cards (
                                        id text PRIMARY KEY,
                                        name text NOT NULL,
                                        desc text,
                                        id_board text NOT NULL,
                                        id_members text, 
                                        labels text,
                                        short_url text,
                                        id_list text,
                                        point real,
                                        due_complete integer
                                    ); """
