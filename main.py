import function.sheet as sheet
import function.pandas as pd

spreadsheet = sheet.open_spreadsheet("Hello world 1")

df = pd.create_dataframe(
    [["hello", "xin chao"], ["hula", "hola"]], columns=["Language", "Country"]
)

ws = sheet.open_worksheet(spreadsheet=spreadsheet, name="Languages")
sheet.fill_data(ws, dataframe=df)
sheet.delete_worksheet(spreadsheet=spreadsheet, name="Sheet1")
