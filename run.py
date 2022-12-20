import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("anna'sclothes")


def calculate_surplus_data():
    """
    Calculate surplus for each item type.
    Surplus is defined as stock - sales.
    0 indicates client missed out on sales due to running out of stock.
    Positive surplus means the items can be counted into next year's stock.
    """
    print("Calculating surplus data\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    sales = SHEET.worksheet("sales").get_all_values()
    sales_row = sales[-1]

    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - int(sales)
        surplus_data.append(surplus)
    return surplus_data

def update_worksheet(data,worksheet):
    """
    Update relevant worksheet
    """
    print(f"Updating {worksheet} worksheet\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n"


def main():
    """
    Run all program functions
    """
    new_surplus_data = calculate_surplus_data()
    update_worksheet(new_surplus_data, "surplus")
    update_worksheet("stock")


main()
