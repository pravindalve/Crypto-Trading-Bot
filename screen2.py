# this screen has bullish kickstarter, atr and then demand ratio
# this screen implements bullish kickstarter and bollinger
import get_positive_coin
# from pyti.bollinger_bands import middle_bollinger_band as mbb
# from pyti.bollinger_bands import lower_bollinger_band as lbb
# from pyti.bollinger_bands import upper_bollinger_band as ubb
from pyti.average_true_range import average_true_range as atr
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from moving_average_convergence_divergence_signal_histogram import macd_signal as macds
from moving_average_convergence_divergence_signal_histogram import macd_histogram as macdh
from binance.client import Client


def screen():
    client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
    positiveCoin = get_positive_coin.positiveCoin
    bullishKScoin = []
    for m in positiveCoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_30MINUTE)
        if candles[-2][1] < candles[-2][4] <= candles[-1][1] < candles[-1][4]:
            bullishKScoin.append(m)


    atrCoin = []
    for m in bullishKScoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_5MINUTE)
        close = []
        for n in candles:
            close.append(float(n[4]))
        avgtr = atr(close, 14)
        if avgtr[-1]/close[-1] > 0.01:
            atrCoin.append(m)


    maxDemandRatio = 0
    buyingCoin = ''
    for m in atrCoin:
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

    if maxDemandRatio < 1.5:
        buyingCoin = ''

    print(bullishKScoin)
    print(atrCoin)
    print(buyingCoin)
    return buyingCoin
