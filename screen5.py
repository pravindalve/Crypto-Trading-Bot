# this screen implements bullish kickstarter, macd growth and bollinger. this screens volatility with bollinger
import get_positive_coin
from pyti.bollinger_bands import percent_b as pbb
from pyti.moving_average_convergence_divergence import moving_average_convergence_divergence as macd
from moving_average_convergence_divergence_signal_histogram import macd_signal as macds
from moving_average_convergence_divergence_signal_histogram import macd_histogram as macdh
from pyti.relative_strength_index import relative_strength_index as rsi
from binance.client import Client


def screen():
    client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
    positiveCoin = get_positive_coin.coin

    bollCoin = []
    for m in positiveCoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_15MINUTE)
        close = []
        for n in candles:
            close.append(float(n[4]))
        pb = pbb(close, 20, 2.0, 2.0)
        if pb[-1] < 10:
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
        if mach[-1] > 0 and (macs[-1] - macs[-2]) < 0 and (mac[-1] - mac[-2]) > 0:
            macdCoin.append(m)

    rsiCoin = []
    for m in macdCoin:
        candles = client.get_klines(symbol=m, interval=client.KLINE_INTERVAL_15MINUTE)
        close = []
        for n in candles:
            close.append(float(n[4]))
        rs = rsi(close, 14)
        if rs[-1] < 30:
            rsiCoin.append(m)
    buyingCoin = ''
    maxDemandRatio = 0
    for m in rsiCoin:
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

    print(bollCoin)
    print(macdCoin)
    print(rsiCoin)
    print(buyingCoin)
    return buyingCoin
