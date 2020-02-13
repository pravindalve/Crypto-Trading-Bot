from binance.client import Client
client = Client("api-key", "api-secret", {"verify": False, "timeout": 20})
tickers = client.get_ticker()
coin = []
for m in tickers:
    coin.append(m['symbol'])
print(coin)
coin1 = []
for m in coin:
    if m[-3:] == 'ETH':
        coin1.append(m)
# print(coin1)
fin_coin = []
for c in coin1:
	fin_coin.append(c[:-3])
print(fin_coin)
print(len(fin_coin))


