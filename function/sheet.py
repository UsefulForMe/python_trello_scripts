import config.sheet as Sheet
import gspread as gs
from modules.user.user_model import User

service, gc = Sheet.init()


def create_spreadsheet(title: str) -> str:
    # title = f"Summary Point {date.today()}"
    spreadsheet = gc.create(title)
    return spreadsheet


def open_spreadsheet(name: str):
    sheet = None
    try:
        sheet = gc.open(name)
    except gs.exceptions.SpreadsheetNotFound as e:
        sheet = create_spreadsheet(name)
    print(sheet.url)
    return sheet


def share_with_many(spreadsheet, users: list["User"]):
    for user in users:
        print(user.email)
        spreadsheet.share(user.email, perm_type="user", role=user.sheet_role)


def open_worksheet(spreadsheet, name: str):
    worksheet = None
    try:
        worksheet = spreadsheet.worksheet(name)

    except gs.exceptions.WorksheetNotFound as e:
        worksheet = spreadsheet.add_worksheet(title=name, rows="100", cols="20")

    return worksheet


def delete_worksheet(spreadsheet, name: str):
    try:
        worksheet_list = spreadsheet.worksheets()
        if len(worksheet_list) <= 1:
            raise "Can not remove all worksheet in spreadsheet"

        worksheet = spreadsheet.worksheet(name)
        spreadsheet.del_worksheet(worksheet)
        return True
    except gs.exceptions.WorksheetNotFound as e:
        raise "Worksheet not found"


def fill_data(worksheet, dataframe):
    try:
        worksheet.update(
            [dataframe.columns.values.tolist()] + dataframe.values.tolist()
        )
    except Exception:
        raise Exception
