import pyperclip

import Parser_v2 as pr
from PyQt5 import QtCore,  QtWidgets
import main
import sys
import json
import requests
import time

class MyWidget(QtWidgets.QMainWindow, pr.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Adres_lineEdit.setCursorPosition(0)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.old_pos = None

        self.first = 0
        self.second = 20

        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(40)

        self.Parse_Button.clicked.connect(self.start_parse)
        self.Copy_Button.clicked.connect(self.copy)

        self.checkBox_USDT.stateChanged.connect(self.check_USDT)
        self.checkBox_BTC.stateChanged.connect(self.check_BTC)

        self.value = 40

    def start_parse(self):
        self.Terminal_TextEdit.setPlainText("Start parsing...")
        self.checkBox_USDT.setEnabled(False)
        self.checkBox_BTC.setEnabled(False)
        if self.first == self.second:
            self.Terminal_TextEdit.appendPlainText("[ERROR]Select fiat !")
            self.checkBox_USDT.setEnabled(True)
            self.checkBox_BTC.setEnabled(True)

        if self.value == 0:
            self.progressBar.setMaximum(1)
        else:
            self.progressBar.setMaximum(self.value)
        self.progressBar.setValue(0)
        self.parse = start_parser(mainwindow=self)
        self.parse.start()

    def check_USDT(self):
        if self.checkBox_USDT.isChecked():
            self.first = 0
            self.Terminal_TextEdit.appendPlainText("USDT on")
            self.value = abs(2 * (self.second - self.first))

        else:
            self.first = 10
            self.Terminal_TextEdit.appendPlainText("USDT off")
            self.value = abs(2 * (self.second - self.first))


    def check_BTC(self):
        if self.checkBox_BTC.isChecked():
            self.second = 20
            self.Terminal_TextEdit.appendPlainText("BTC on")
            self.value = abs(2 * (self.second - self.first))

        else:
            self.second = 10
            self.Terminal_TextEdit.appendPlainText("BTC off")
            self.value = abs(2 * (self.second - self.first))


    def copy(self):
        adres = self.Adres_lineEdit.text()
        pyperclip.copy(adres)
        self.Terminal_TextEdit.appendPlainText("Address copied to clipboard")

    # вызывается при нажатии кнопки мыши
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = event.pos()

    # вызывается при отпускании кнопки мыши
    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.old_pos = None

    # вызывается всякий раз, когда мышь перемещается
    def mouseMoveEvent(self, event):
        if not self.old_pos:
            return
        delta = event.pos() - self.old_pos
        self.move(self.pos() + delta)

class start_parser(QtCore.QThread):
    def __init__(self, mainwindow, parent=None):
        super().__init__()
        self.mainwindow = mainwindow

    def run(self):
        try:
            self.fill_table()
        except:
            self.mainwindow.Terminal_TextEdit.appendPlainText("[ERROR] Please, try again!")
            self.mainwindow.Parse_Button.setText("Parse")
            self.mainwindow.Parse_Button.setEnabled(True)
            self.mainwindow.checkBox_USDT.setEnabled(True)
            self.mainwindow.checkBox_BTC.setEnabled(True)

    def data_Binance(self, x, count):
        with open('sites.json', encoding='UTF-8') as file:
            data = json.loads(file.read())
            payTypes = data['data'][x]['payTypes']
            TradeType = data['data'][x]['tradeType']
            asset = data['data'][x]['asset']

            headers = {
                'authority': 'p2p.binance.com',
                'accept': '*/*',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'bnc-uuid': '1325752c-a715-461b-99a5-e4bda1bf6f13',
                'c2ctype': 'c2c_merchant',
                'clienttype': 'web',
                'csrftoken': '',
                'device-info': '',
                'fvideo-id': '33ebcfe5d8a7a8ccbe33c755a9daf613516d4b8b',
                'lang': 'ru',
                'origin': 'https://p2p.binance.com',
                'referer': 'https://p2p.binance.com/ru/trade/sell/USDT?fiat=RUB&payment=Tinkoff',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
                'x-trace-id': '',
                'x-ui-request-trace': '',
            }

            json_data = {
                'page': 1,
                'rows': 10,
                'payTypes': [
                    payTypes,
                ],
                'countries': [],
                'publisherType': None,
                'asset': asset,
                'fiat': 'RUB',
                'tradeType': TradeType,
            }

            response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers,
                                     json=json_data)
            str = json.dumps(response.json(), indent=4, ensure_ascii=False)
            obj = json.loads(str)

            price = float(obj['data'][0]['adv']['price'])
            price2 = float(obj['data'][1]['adv']['price'])
            fiat = obj['data'][0]['adv']['fiatUnit']
            TradeType = obj['data'][0]['adv']['tradeType']

            if TradeType == 'SELL':
                TradeType = 'Купить'
            else:
                TradeType = 'Продать'

            terminal = f"[{count}/{self.mainwindow.value}]{asset}:{price} {fiat}   Стакан:{TradeType}  Платежная система:{payTypes}"

            self.mainwindow.Terminal_TextEdit.appendPlainText(terminal)

        return price, price2

    def fill_table(self):
        self.mainwindow.Parse_Button.setText("Parsing...")
        self.mainwindow.Parse_Button.setEnabled(False)

        self.n = 0

        for y in range(0, 2):
            list = {0: {0: "B6", 1: "E6"}, 1: {0: "C6", 1: "F6"}, 2: {0: "B7", 1: "E7"}, 3: {0: "C7", 1: "F7"}, 4: {0: "B8", 1: "E8"},
                    5: {0: "C8", 1: "F8"}, 6: {0: "B9", 1: "E9"}, 7: {0: "C9", 1: "F9"}, 8: {0: "B10", 1: "E10"}, 9: {0: "C10", 1: "F10"},
                    10: {0: "I6", 1: "L6"}, 11: {0: "J6", 1: "M6"}, 12: {0: "I7", 1: "L7"}, 13: {0: "J7", 1: "M7"}, 14: {0: "I8", 1: "L8"},
                    15: {0: "J8", 1: "M8"}, 16: {0: "I9", 1: "L9"}, 17: {0: "J9", 1: "M9"}, 18: {0: "I10", 1: "L10"}, 19: {0: "J10", 1: "M10"}}

            for x in range(self.mainwindow.first, self.mainwindow.second):
                self.n += 1

                cell = "Binance_P2P!" + list[x][y]
                price, price2 = self.data_Binance(x, self.n)
                data = [[(price, price2)[y]]]  # <-- y = number_price
                main.sheet.values().update(spreadsheetId=main.sheet_id, range=cell, valueInputOption="USER_ENTERED", body={"values": data}).execute()

                self.mainwindow.progressBar.setValue(self.n)

        main.write_datetime()

        time.sleep(3)

        self.mainwindow.Terminal_TextEdit.appendPlainText("Дата: " + str(main.write_datetime()))

        self.mainwindow.Parse_Button.setText("Parse")
        self.mainwindow.Parse_Button.setEnabled(True)

        self.mainwindow.checkBox_USDT.setEnabled(True)
        self.mainwindow.checkBox_BTC.setEnabled(True)

        self.mainwindow.Terminal_TextEdit.appendPlainText("Finish parsing !")
        self.mainwindow.Terminal_TextEdit.setFocus()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = MyWidget()
    w.show()
    sys.exit(app.exec_())