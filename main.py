#  STEP 1 -Import the necessary libraries

import cbpro, datetime, numpy, time
 
#  STEP 2 - GET AUTHORIZED

apiKey = 'your api key here'
apiSecret = 'your api secret here'
passphrase = 'passphrase goes here'
auth_client = cbpro.AuthenticatedClient(apiKey,apiSecret,passphrase)


# STEP 3 -  Pick a pair to trade 

coin = input('Coin:'+'')
fiat = input('Fiat:'+'')
currency = (coin+'-'+fiat)

#  STEP 4 - Get the ID's for the chosen pair 

def account(iD):
 for account in auth_client.get_accounts():
  if account['currency'] == iD:
   return account['id']

# STEP 5 - Get the chosen pair's current price

startingPrice = float(auth_client.get_product_ticker(product_id=currency)['price'])

# STEP 6 - Get the chosen pair's current balances
startingCoin = float(auth_client.get_account(account(coin[:3]))['available'])
startingDollar = float(auth_client.get_account(account(fiat[:3]))['available'])
startingValue = float(startingDollar + (startingCoin * startingPrice))

#  STEP 7 - Set the prices to later distinguish high from low and make profitable trades.

lastBuy = startingPrice
lastSell = startingPrice

# STEP 8 - Set soldLast to none so that we start looking to buy or sell, turn of later to prevent double sell.

soldLast = None

# STEP 9 - Iinitaite the loop, start iteration count, and trade count, begin loop.

trade = True
tradeCount = 0
iteration = 0
sell = True
buy = True
while trade == True:
  
# STEP 10 - Count a new iteration define fee(desired gain), price, funding, portfolio value, and running total of profit 
  
    iteration += 1
    fee = (0.0055)
    price = float(auth_client.get_product_ticker(product_id=currency)['price'])
    x  = float(auth_client.get_account(account(coin[:3]))['available'])
    owned = int(x)
    y = float(auth_client.get_account(account(fiat[:3]))['available'])
    funding = int(y)
    currentValue = float(y + (owned * price))
    profit = round((currentValue - startingValue),5)
    desiredBuy = float(lastSell - (lastSell * fee))
    desiredSell = float(lastBuy + (lastBuy * fee))
    buySignal = (price < desiredBuy)
    sellSignal = (price > desiredSell)
# STEP 11 - Place a market sell order if the onditions are met, then tell me, update soldlast variable, turn sell off and buy on, count the new trade.
    
    if sellSignal == True and sell == True:
      auth_client.place_market_order(product_id = currency, side='sell', size = str(owned))
      lastSell =  float(auth_client.get_product_ticker(product_id=currency)['price'])
      print('sell!')
      tradeCount += 1
      sell = False
      buy = True
            
# STEP 12 - Place a market buy order if the onditions are met, then tell me, update soldlast variable,turn buy off and sell on, count the new trade.

    if buySignal == True and buy == True:
      auth_client.place_market_order(product_id = currency, side='buy', funds = str(funding))
      lastBuy =  float(auth_client.get_product_ticker(product_id=currency)['price'])
      print('buy!')
      tradeCount += 1
      sell = True
      buy = False
            
# STEP 13 - Tell me all about everything

    print(currency,
          iteration,
          fiat,':', funding,
          coin,':', owned,
          'price:', price,
          'lastBuy:',lastBuy,
          'lastSell', lastSell,
          'tradeCount:', tradeCount,          
          'buySignal:', buySignal,
          'sellSignal:', sellSignal,
          'startingValue:',startingValue,
          'currentValue:', currentValue,
          'profit:', profit
          )
    
# STEP 14 - Take a few seconds to breathe, then do it again.
    
    time.sleep(10)
