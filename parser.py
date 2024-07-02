import json
import requests


def data_Binance(x, count):
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

            response = requests.post('https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search', headers=headers, json=json_data)
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

            terminal = f"[{count}]{asset}:{price} {fiat}   Стакан:{TradeType}  Платежная система:{payTypes}"

            print(terminal)

        return price, price2

if __name__ == '__main__':
    print("fad")
    # data_Binance()


