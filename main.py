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

while trade == True:
  
# STEP 10 - Count a new iteration define fee(desired gain), price, funding, portfolio value, and running total of profit 
  
    iteration += 1
    fee = (0.01)
    price = float(auth_client.get_product_ticker(product_id=currency)['price'])
    x = float(auth_client.get_account(account(coin[:3]))['available'])
    owned = round(x-(x*0.25),2)
    y = float(auth_client.get_account(account(fiat[:3]))['available'])
    funding = round(y-1,2)
    currentValue = float(y + (x * price))
    profit = round((currentValue - startingValue),5)
    
# STEP 11 - Place a market sell order if the onditions are met, then tell me, update soldlast variable, count the new trade.
    
    if (price > lastBuy + (lastBuy * fee)):
        if soldLast == False or None:
            auth_client.place_market_order(product_id = currency, side='sell', size = str(owned))
            lastSell =  float(auth_client.get_product_ticker(product_id=currency)['price'])
            print('sell!')
            soldLast = True
            tradeCount += 1
            
# STEP 12 - Place a market buy order if the onditions are met, then tell me, update soldlast variable, count the new trade.

    if (price < lastBuy - (lastBuy * fee)):
        if soldLast == True or None:
            auth_client.place_market_order(product_id = currency, side='buy', funds = str(funding))
            lastBuy =  float(auth_client.get_product_ticker(product_id=currency)['price'])
            print('buy!')
            soldLast = False
            tradeCount += 1
            
# STEP 13 - Tell me all about everything

    print(currency,
          'dollar:', y,
          'coin:', x,
          'starting value:',startingValue,
          'current value:', currentValue,
          'profit:', profit,
          'last sell', lastSell,
          'desired buy:',(lastBuy - (lastBuy * fee)),
          'price:', price,
          'lastBuy:',lastBuy,
          'desiredSell:',(lastBuy + (lastBuy * fee)),
          'tradeCount:', tradeCount,
          'iteration', iteration)
    
# STEP 14 - Take a few seconds to breathe, then do it again.
    
    time.sleep(10)
