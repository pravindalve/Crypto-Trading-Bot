from binance.client import Client

client = Client("api-key", "api-secret", {"verify": False, "timeout": 100})
coin = ['QTUMETH', 'EOSETH', 'SNTETH', 'BNTETH', 'BNBETH', 'OAXETH', 'DNTETH', 'MCOETH', 'ICNETH', 'WTCETH', 'LRCETH',
        'OMGETH', 'ZRXETH', 'STRATETH', 'SNGLSETH', 'BQXETH', 'KNCETH', 'FUNETH', 'SNMETH', 'NEOETH', 'IOTAETH',
        'LINKETH', 'XVGETH', 'CTRETH', 'SALTETH', 'MDAETH', 'MTLETH', 'SUBETH', 'ETCETH', 'MTHETH', 'ENGETH', 'ZECETH',
        'ASTETH', 'DASHETH', 'BTGETH', 'EVXETH', 'REQETH', 'VIBETH', 'HSRETH', 'TRXETH', 'POWRETH', 'ARKETH', 'YOYOETH',
        'XRPETH', 'MODETH', 'ENJETH', 'STORJETH', 'VENETH', 'KMDETH', 'RCNETH', 'NULSETH', 'RDNETH', 'XMRETH', 'DLTETH',
        'AMBETH', 'BCCETH', 'BATETH', 'BCPTETH', 'ARNETH', 'GVTETH', 'CDTETH', 'GXSETH', 'POEETH', 'QSPETH', 'BTSETH',
        'XZCETH', 'LSKETH', 'TNTETH', 'FUELETH', 'MANAETH', 'BCDETH', 'DGDETH', 'ADXETH', 'ADAETH', 'PPTETH', 'CMTETH',
        'XLMETH', 'CNDETH', 'LENDETH', 'WABIETH', 'LTCETH', 'TNBETH', 'WAVESETH', 'GTOETH', 'ICXETH', 'OSTETH',
        'ELFETH', 'AIONETH', 'NEBLETH', 'BRDETH', 'EDOETH', 'WINGSETH', 'NAVETH', 'LUNETH', 'TRIGETH', 'APPCETH',
        'VIBEETH', 'RLCETH', 'INSETH', 'PIVXETH', 'IOSTETH', 'CHATETH', 'STEEMETH', 'NANOETH', 'VIAETH', 'BLZETH',
        'AEETH', 'RPXETH', 'NCASHETH', 'POAETH']
tickers = client.get_ticker()
positiveCoin = []
percentChange = []
for m in tickers:
    for n in coin:
        if m['symbol'] == n and float(m['priceChangePercent']) > 0:
            positiveCoin.append(n)
            percentChange.append(m['priceChangePercent'])
print(positiveCoin)
print(percentChange)
