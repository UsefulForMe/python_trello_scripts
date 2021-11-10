class User:
    def __init__(self, id, name, email, sheet_role):
        self.id = id
        self.name = name
        self.email = email
        self.sheet_role = sheet_role

    @staticmethod
    def from_json(json_data):
        return User(
            json_data["id"],
            json_data["name"],
            json_data["email"],
            json_data["sheet_role"],
        )

    @staticmethod
    def from_puple(puple):
        return User(
            puple[0],
            puple[1],
            puple[2],
            puple[3],
        )

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "sheet_role": self.sheet_role,
        }

    def to_puple(self):
        return (
            self.id,
            self.name,
            self.email,
            self.sheet_role,
        )


sql_create_user_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id text PRIMARY KEY,
                                        name text NOT NULL,
                                        email text NOT NULL,
                                        sheet_role text NOT NULL
                                        ); """
