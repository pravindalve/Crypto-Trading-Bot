# this screen implements bullish kickstarter, bollinger. this screens detects volatility with bollinger
import get_positive_coin
from pyti.bollinger_bands import percent_b as pbb
from pyti.bollinger_bands import upper_bollinger_band as ubb
from pyti.bollinger_bands import lower_bollinger_band as lbb
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from moving_average_convergence_divergence_signal_histogram import macd_signal as macds
from moving_average_convergence_divergence_signal_histogram import macd_histogram as macdh
from binance.client import Client


def screen():
    client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
    positiveCoin = get_positive_coin.positiveCoin


    bollCoin = []
    for m in positiveCoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_15MINUTE)
        close = []
        for n in candles:
            close.append(float(n[4]))
        pb = pbb(close, 20, 2.0, 2.0)
        lb = lbb(close, 20, 2.0)
        ub = ubb(close, 20, 0.2)
        if pb[-1] < 50 and ((ub[-1] - lb[-1]) / lb[-1]) > 0.03:
            bollCoin.append(m)

    macdCoin = []
    for m in bollCoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_5MINUTE)
        close = []
        for n in candles:
            close.append(float(n[4]))
        mac = macd(close, 12, 26)
        macs = macds(mac)
        mach = macdh(mac, macs)
        # if mach[-1] > 0 and (macs[-1] - macs[-2]) > 0 and (mac[-1] - mac[-2]) > 0:
        #     macdCoin.append(m)
        if mach[-1] > 0 and (macs[-1] - macs[-2]) > 0 and (mac[-1] - mac[-2]) > 0:
            macdCoin.append(m)

    bullishKSCoin = []
    for m in macdCoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_5MINUTE)
        if candles[-2][1] < candles[-2][4]:
            if candles[-2][4] <= candles[-1][1]:
                if candles[-1][1] < candles[-1][4]:
                    bullishKSCoin.append(m)


    buyingCoin = ''
    maxDemandRatio = 0
    for m in bullishKSCoin:
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


    print(bollCoin)
    print(macdCoin)
    print(bullishKSCoin)
    print(buyingCoin)
    return buyingCoin
