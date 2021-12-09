import pandas as pd
import sqlite3
import datetime as DateTime
import sys
import pyperclip

print(sys.argv)

conn = sqlite3.connect(
    "db.sql", isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES
)

query_user = "1==1" if sys.argv[1] == "all" else f"users.email like '%{sys.argv[1]}%'"
first_week_of_last_month = int(sys.argv[2])
last_week_of_last_month = int(sys.argv[3])


db_df = pd.read_sql_query(
    f"""
    SELECT users.name as username,cards.name,labels,short_url,point,week FROM cards JOIN users ON cards.id_member = users.id 
    WHERE 
        {query_user} AND
        cards.week BETWEEN {first_week_of_last_month} AND {last_week_of_last_month}
    """,
    conn,
)
db_df.to_csv("database.csv", index=False)

# copy content of database.csv to clipboard with format of excel with column names
pyperclip.copy(
    db_df.to_csv(
        index=False,
        sep="\t",
        encoding="utf-8",
        columns=["username", "name", "labels", "short_url", "point", "week"],
    )
)
