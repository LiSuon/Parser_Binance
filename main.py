import os
import json
from parser import data_Binance
import datetime

import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials


def main(x):
    with open('sites.json', encoding='UTF-8') as file:
        data = json.loads(file.read())
        name = data['data'][x]['tradeType']
    return name

# Функция авторизации
def get_service_sacc():
    creds_json = os.path.dirname(__file__) + "/credentials.json"
    scopes = ['https://www.googleapis.com/auth/spreadsheets']

    creds_service = ServiceAccountCredentials.from_json_keyfile_name(creds_json, scopes).authorize(httplib2.Http())
    return build('sheets', 'v4', http=creds_service)

service = get_service_sacc()
sheet = service.spreadsheets()

sheet_id = "1AA34T69zhsKM7dX3FqonW1v6SbLODFtHqF4tNoiyK_U"

# Дата
def write_datetime():
    date = str(datetime.datetime.today())
    res_date = date[:19]
    data = [[res_date]]
    sheet.values().update(spreadsheetId=sheet_id,
                          range="Binance_P2P!B1",
                          valueInputOption="USER_ENTERED",
                          body={"values": data}).execute()
    return res_date

# Отправка данных в таблицу
def fill_table():
    terminal = None
    for y in range(0, 2):
        list = {0: {0: "B6", 1: "E6"}, 1: {0: "C6", 1: "F6"}, 2: {0: "B7", 1: "E7"}, 3: {0: "C7", 1: "F7"}, 4: {0: "B8", 1: "E8"},
                5: {0: "C8", 1: "F8"}, 6: {0: "B9", 1: "E9"}, 7: {0: "C9", 1: "F9"}, 8: {0: "B10", 1: "E10"}, 9: {0: "C10", 1: "F10"},
                10: {0: "I6", 1: "L6"}, 11: {0: "J6", 1: "M6"}, 12: {0: "I7", 1: "L7"}, 13: {0: "J7", 1: "M7"}, 14: {0: "I8", 1: "L8"},
                15: {0: "J8", 1: "M8"}, 16: {0: "I9", 1: "L9"}, 17: {0: "J9", 1: "M9"}, 18: {0: "I10", 1: "L10"}, 19: {0: "J10", 1: "M10"}}
        for x in range(0, 20):

            if y < 1:
                count = str(x + 1) + "/40"
            else:
                count = str(x + 21) + "/40"

            cell = "Binance_P2P!" + list[x][y]
            price, price2 = data_Binance(x, count)
            data = [[(price, price2)[y]]]  # <-- y = number_price
            sheet.values().update(spreadsheetId=sheet_id, range=cell, valueInputOption="USER_ENTERED", body={"values": data}).execute()
    write_datetime()
    print("Дата: " + str(write_datetime()))
    return terminal

if __name__ == '__main__':
    fill_table()