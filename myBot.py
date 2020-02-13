import pandas as pd
from screen2 import screen as screen
from time import strftime, sleep, localtime

from binance.client import Client

client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
coin = ['QTUM', 'EOS', 'SNT', 'BNT', 'BNB', 'OAX', 'DNT', 'MCO', 'ICN', 'WTC', 'LRC', 'OMG', 'ZRX', 'STRAT',
        'SNGLS', 'BQX', 'KNC', 'FUN', 'SNM', 'NEO', 'IOTA', 'LINK', 'XVG', 'SALT', 'MDA', 'MTL', 'SUB',
        'ETC', 'MTH', 'ENG', 'ZEC', 'AST', 'DASH', 'BTG', 'EVX', 'REQ', 'VIB', 'HSR', 'TRX', 'POWR', 'ARK',
        'YOYO', 'XRP', 'MOD', 'ENJ', 'STORJ', 'VEN', 'KMD', 'RCN', 'NULS', 'RDN', 'XMR', 'DLT', 'AMB', 'BCC',
        'BAT', 'BCPT', 'ARN', 'GVT', 'CDT', 'GXS', 'POE', 'QSP', 'BTS', 'XZC', 'LSK', 'TNT', 'FUEL', 'MANA',
        'BCD', 'DGD', 'ADX', 'ADA', 'PPT', 'CMT', 'XLM', 'CND', 'LEND', 'WABI', 'LTC', 'TNB', 'WAVES', 'GTO',
        'ICX', 'OST', 'ELF', 'AION', 'NEBL', 'BRD', 'EDO', 'WINGS', 'NAV', 'LUN', 'TRIG', 'APPC', 'VIBE',
        'RLC', 'INS', 'PIVX', 'IOST', 'CHAT', 'STEEM', 'NANO', 'VIA', 'BLZ', 'AE', 'RPX', 'NCASH', 'POA',
        'ZIL', 'ONT', 'STORM', 'XEM', 'WAN', 'WPR', 'QLC', 'SYS', 'GRS', 'CLOAK', 'GNT', 'LOOM', 'BCN',
        'REP', 'TUSD', 'ZEN', 'SKY', 'CVC', 'THETA', 'IOTX', 'QKC', 'AGI', 'NXS', 'DATA', 'SC', 'NPXS',
        'KEY', 'NAS', 'MFT', 'DENT', 'ARDR', 'HOT', 'VET', 'DOCK', 'PHX', 'HC', 'PAX']

balance = []
for i in range(0, 146, 1):
    balance.append(0.0)
print(balance)
wal = {'coinname': coin, 'balance': balance}
wall = pd.DataFrame(wal)
wallet = wall.set_index('coinname')
print(wallet)
etherVol = 0.05
tradedCoin = 'ETH'
tradedVol = 0.05
initialEth = 0.05
f = open("Trades.txt", "w+")
f.close()
buyC = ''
sellPrice = 0.0

while True:
    if tradedCoin == 'ETH':
        buyC = screen()
        if buyC == '':
            t = strftime("%Y-%m-%d %H:%M:%S", localtime())
            f = open("Trades.txt", "a")
            f.write('At ' + t + ' Could not find anything\n')
            f.close()
        else:
            trade = client.get_aggregate_trades(symbol=buyC)
            tradedVol = etherVol / float(trade[-1]['p'])
            print(wallet)
            wallet.at[buyC[:-3], 'balance'] = etherVol / float(trade[-1]['p'])
            print(wallet)
            tradedCoin = buyC[:-3]
            etherVol = 0.0
            t = strftime("%Y-%m-%d %H:%M:%S", localtime())
            f = open("Trades.txt", "a")
            f.write('At ' + t + ' ' + str(tradedVol) + ' ' + buyC[:-3] + ' bought at ' + trade[-1]['p'] + '.\n')
            f.close()
            sellPrice = float(trade[-1]['p']) * 1.001
    else:
        trade = client.get_aggregate_trades(symbol=buyC)
        if float(trade[-1]['p']) >= sellPrice:
            updatedCoin = screen()
            print(updatedCoin[:-3])
            print(tradedCoin)
            if updatedCoin[:-3] == tradedCoin:
                sellPrice = sellPrice * 1.00002
                f = open('Trades.txt', 'a')
                f.write(updatedCoin[:-3] + ' came again so holding it.\n')
                f.write('Waiting for selling price to become ' + str(sellPrice) + '\n')
                f.close()
            else:
                etherVol = float(trade[-1]['p']) * tradedVol
                wallet.at[buyC, 'balance'] = 0.0
                print(wallet)
                print(trade[-1]['p'])
                tradedCoin = 'ETH'
                tradedVol = etherVol
                t = strftime("%Y-%m-%d %H:%M:%S", localtime())
                f = open("Trades.txt", 'a')
                f.write('At ' + t + ' ' + str(tradedVol) + ' ' + buyC[:-3] + ' sold at ' + trade[-1]['p'] + '.\n')
                f.write('Overall Profit: ' + str((etherVol - initialEth) * 100 / initialEth) + '%\n')
                f.close()
        elif float(trade[-1]['p']) <= sellPrice * 0.98:
            updatedCoin = screen()
            print(updatedCoin[:-3])
            print(tradedCoin)
            if updatedCoin[:-3] == tradedCoin:
                f = open('Trades.txt', 'a')
                f.write('Again ' + updatedCoin[:-3] + ' came so holding ' + updatedCoin[:-3] + '.\n')
                f.write('Waiting for selling price to become ' + str(sellPrice) + '.\n')
                f.close()
            else:
                etherVol = float(trade[-1]['p']) * tradedVol
                wallet.at[buyC, 'balance'] = 0.0
                print(wallet)
                print(trade[-1]['p'])
                t = strftime("%Y-%m-%d %H:%M:%S", localtime())
                f = open("Trades.txt", 'a')
                f.write('At ' + t + ' ' + str(tradedVol) + ' ' + buyC[:-3] + ' sold in a loss at ' + trade[-1]['p'] + '.\n')
                f.write('Overall profit: ' + str((etherVol - initialEth) * 100 / initialEth) + '%\n')
                f.close()
                tradedCoin = 'ETH'
                tradedVol = etherVol
    sleep(5)
