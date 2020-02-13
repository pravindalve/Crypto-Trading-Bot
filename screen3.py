# this screen implements bullish kickstarter, macd growth and bollinger. this screens volatility with bollinger
import get_positive_coin
from pyti.bollinger_bands import middle_bollinger_band as mbb
from pyti.bollinger_bands import lower_bollinger_band as lbb
from pyti.bollinger_bands import upper_bollinger_band as ubb
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

    macdCoin = []
    # for m in bullishKScoin:
    #     candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_1HOUR)
    #     close = []
    #     for n in candles:
    #         close.append(float(n[4]))
    #     mac = macd(close, 12, 26)
    #     macs = macds(mac)
    #     mach = macdh(mac, macs)
    #     # if mach[-1] > 0 and (macs[-1] - macs[-2]) > 0 and (mac[-1] - mac[-2]) > 0:
    #     #     macdCoin.append(m)
    #     if mach[-1] > 0 and (macs[-1] - macs[-2]) > 0 and (mac[-1] - mac[-2]) > 0:
    #         macdCoin.append(m)

    bollCoin = []
    for m in bullishKScoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_1HOUR)
        close = []
        for n in candles:
            close.append(float(n[4]))
        lb = lbb(close, 20, 2)
        mb = mbb(close, 20, 2)
        ub = ubb(close, 20, 2)

        if ((ub[-1] - lb[-1])/lb[-1]) > 0.1:
            bollCoin.append(m)

    maxDemandRatio = 0
    buyingCoin = ''
    for m in bollCoin:
        depth = client.get_order_book(symbol=m)
        buyingVol = 0
        sellingVol = 0
        for n in depth['bids'][0:30]:
            buyingVol = buyingVol + float(n[1])
        for n in depth['asks'][0:30]:
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
    print(macdCoin)
    print(bollCoin)
    print(buyingCoin)
    return buyingCoin
