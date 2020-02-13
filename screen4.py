# this screen have bollinger percent band, bullish kickstarter and demand ratio
import get_positive_coin
from pyti.bollinger_bands import percent_b as pbb

from binance.client import Client


def screen():
    client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
    positiveCoin = get_positive_coin.positiveCoin

    pbCoin = []
    for m in positiveCoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_15MINUTE)
        close = []
        for n in candles:
            close.append(float(n[4]))
        pb = pbb(close, 20, 2.0, 2.0)
        if 50 > pb[-1] > 10:
            pbCoin.append(m)


    # bullishKScoin = []
    # for m in pbCoin:
    #     candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_30MINUTE)
    #     if candles[-2][1] < candles[-2][4] <= candles[-1][1] < candles[-1][4]:
    #         bullishKScoin.append(m)


    maxDemandRatio = 0
    buyingCoin = ''
    for m in pbCoin:
        depth = client.get_order_book(symbol=m)
        buyingVol = 0
        sellingVol = 0
        for n in depth['bids'][0:20]:
            buyingVol = buyingVol + float(n[1])
        for n in depth['asks'][0:20]:
            sellingVol = sellingVol + float(n[1])
        demandRatio = buyingVol / sellingVol
        print(demandRatio)
        print(maxDemandRatio)
        if demandRatio > maxDemandRatio:
            maxDemandRatio = demandRatio
            buyingCoin = m

    if maxDemandRatio < 1:
        buyingCoin = ''

    print(pbCoin)
    print(buyingCoin)
    return buyingCoin
