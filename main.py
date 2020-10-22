
#  STEP 1 -Import the necessary libraries

import cbpro
import time
import numpy as np
import datetime as dt
#  STEP 2 - GET AUTHORIZED

apiKey = 'your api key here'
apiSecret = 'your api secret here'
passphrase = 'passphrase goes here'
auth_client = cbpro.AuthenticatedClient(apiKey,apiSecret,passphrase)

# STEP 3 -  Pick a pair to trade

coin = input('      Enter coin :'+'').upper()
fiat = input('      Enter native currency:'+'').upper()
currency = (coin+'-'+fiat)
granularity = input('      granularity (60,300,900,3600):'+'')
gran = int(granularity)
nerdStats = input('      NerdStats? yes or no:'+'').upper()


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

lastBuy = (startingPrice - (startingPrice * 0.01))
lastSell = (startingPrice + (startingPrice * 0.01))
# we start looking to buy, .
if (startingDollar > 10):
  buy = True
  sell = False
if (startingCoin * startingPrice > 10):
  buy = False
  sell = True


# STEP 9 - Iinitaite the loop, start iteration count, and trade count, begin loop.

trade = True
trdCnt = 0
iteration = 0

while trade == True:
  
# STEP 10 - Count a new iteration define fee(desired gain), price, funding, portfolio value, and running total of profit 
  
    iteration += 1
    fee = (0.01)
    price = float(auth_client.get_product_ticker(product_id=currency)['price'])
    x  = float(auth_client.get_account(account(coin[:3]))['available'])
    owned = int(x)
    xx = (x - (x*0.0001))
    sellDat= round((xx),2)
    y = float(auth_client.get_account(account(fiat[:3]))['available'])
    funding = int(y)
    currentValue = float(y + (x * price))
    profit = round((currentValue - startingValue),5)
    desiredBuy = float(lastSell - (lastSell * fee))
    desiredSell = float(lastBuy + (lastBuy * fee))
    buySignal = (price < desiredBuy)
    sellSignal = (price > desiredSell)
# STEP 11 - Place a market sell order if the onditions are met, then tell me, update soldlast variable, turn sell off and buy on, count the new trade.

    historicData = auth_client.get_product_historic_rates(currency, granularity=gran)

        # Make an array of the historic price data from the matrix
    p = np.squeeze(np.asarray(np.matrix(historicData)[:,4]))

        # Wait for 1 second, to avoid API limit
    time.sleep(1)

        # Get latest data and show to the user for reference
    newData = auth_client.get_product_ticker(product_id=currency)
    
    currentPrice=newData['price']
    
    # Calculate the rate of change 11 and 14 units back, then sum them
    ROC11 = np.zeros(13)
    ROC14 = np.zeros(13)
    ROCSUM = np.zeros(13)

    for ii in range(0,13):
        ROC11[ii] = (100*(p[ii]-p[ii+11]) / float(p[ii+11]))
        ROC14[ii] = (100*(p[ii]-p[ii+14]) / float(p[ii+14]))
        ROCSUM[ii] = ( ROC11[ii] + ROC14[ii] )

    # Calculate the past 4 Coppock values with Weighted Moving Average
    coppock = np.zeros(4)
    for ll in range(0,4):
        coppock[ll] = (((1*ROCSUM[ll+9]) + (2*ROCSUM[ll+8]) + (3*ROCSUM[ll+7]) \
        + (4*ROCSUM[ll+6]) + (5*ROCSUM[ll+5]) + (6*ROCSUM[ll+4]) \
        + (7*ROCSUM[ll+3]) + (8*ROCSUM[ll+2]) + (9*ROCSUM[ll+1]) \
        + (10*ROCSUM[ll])) / float(55))

    # Calculate the past 3 derivatives of the Coppock Curve
    coppockD1 = np.zeros(3)
    for mm in range(3):
        coppockD1[mm] = coppock[mm] - coppock[mm+1]


      
    if (coppockD1[0]/abs(coppockD1[0])) == 1.0 and (coppockD1[1]/abs(coppockD1[1])) == -1.0:
      signal = True
    else:
      signal = False
      

    if signal == True and sellSignal == True and sell == True:
      print(auth_client.place_market_order(product_id = currency, side='sell', size = str(sellDat)))
      lastSell =  float(auth_client.get_product_ticker(product_id=currency)['price'])
      
      trdCnt += 1
      sell = False
      buy = True
            
# STEP 12 - Place a market buy order if the onditions are met, then tell me, update soldlast variable,turn buy off and sell on, count the new trade.

    if signal == True and  buySignal == True and buy == True:
      print(auth_client.place_market_order(product_id = currency, side='buy', funds = str(funding)))
      lastBuy =  float(auth_client.get_product_ticker(product_id=currency)['price'])
      
      trdCnt += 1
      sell = True
      buy = False

            
# STEP 13 - Tell me all about everything
    if nerdStats == str( 'YES'):
        print('\n',iteration,
            'trades:', trdCnt,
            '|bet:', desiredBuy,
            '|price:', price,
            '|ditch:',desiredSell,
            '|had:',startingValue,
            '|have:',currentValue,
            '|earned:',profit,
            '|balances:',owned,fiat,funding,
            '|decision making: buy-', buy,
              'sell-',sell,'execute-',signal,'\n')

    if nerdStats == str( 'NO' ):
      print(iteration)
# STEP 14 - Take a few seconds to breathe, then do it again.
    
    time.sleep(15)
if (startingCoin * startingPrice > 10):
  buy = False
  sell = True


# STEP 9 - Iinitaite the loop, start iteration count, and trade count, begin loop.

trade = True
trdCnt = 0
iteration = 0

while trade == True:
  
# STEP 10 - Count a new iteration define fee(desired gain), price, funding, portfolio value, and running total of profit 
  
    iteration += 1
    fee = (0.01)
    price = float(auth_client.get_product_ticker(product_id=currency)['price'])
    x  = float(auth_client.get_account(account(coin[:3]))['available'])
    owned = int(x)
    xx = (x - (x*0.0001))
    sellDat= round((xx),2)
    y = float(auth_client.get_account(account(fiat[:3]))['available'])
    funding = int(y)
    currentValue = float(y + (x * price))
    profit = round((currentValue - startingValue),5)
    desiredBuy = float(lastSell - (lastSell * fee))
    desiredSell = float(lastBuy + (lastBuy * fee))
    buySignal = (price < desiredBuy)
    sellSignal = (price > desiredSell)
# STEP 11 - Place a market sell order if the onditions are met, then tell me, update soldlast variable, turn sell off and buy on, count the new trade.

    historicData = auth_client.get_product_historic_rates(currency, granularity=300)

        # Make an array of the historic price data from the matrix
    p = np.squeeze(np.asarray(np.matrix(historicData)[:,4]))

        # Wait for 1 second, to avoid API limit
    time.sleep(1)

        # Get latest data and show to the user for reference
    newData = auth_client.get_product_ticker(product_id=currency)
    
    currentPrice=newData['price']
    
    # Calculate the rate of change 11 and 14 units back, then sum them
    ROC11 = np.zeros(13)
    ROC14 = np.zeros(13)
    ROCSUM = np.zeros(13)

    for ii in range(0,13):
        ROC11[ii] = (100*(p[ii]-p[ii+11]) / float(p[ii+11]))
        ROC14[ii] = (100*(p[ii]-p[ii+14]) / float(p[ii+14]))
        ROCSUM[ii] = ( ROC11[ii] + ROC14[ii] )

    # Calculate the past 4 Coppock values with Weighted Moving Average
    coppock = np.zeros(4)
    for ll in range(0,4):
        coppock[ll] = (((1*ROCSUM[ll+9]) + (2*ROCSUM[ll+8]) + (3*ROCSUM[ll+7]) \
        + (4*ROCSUM[ll+6]) + (5*ROCSUM[ll+5]) + (6*ROCSUM[ll+4]) \
        + (7*ROCSUM[ll+3]) + (8*ROCSUM[ll+2]) + (9*ROCSUM[ll+1]) \
        + (10*ROCSUM[ll])) / float(55))

    # Calculate the past 3 derivatives of the Coppock Curve
    coppockD1 = np.zeros(3)
    for mm in range(3):
        coppockD1[mm] = coppock[mm] - coppock[mm+1]


      
    if (coppockD1[0]/abs(coppockD1[0])) == 1.0 and (coppockD1[1]/abs(coppockD1[1])) == -1.0:
      signal = True
    else:
      signal = False
      

    if signal == True and sellSignal == True and sell == True:
      print(auth_client.place_market_order(product_id = currency, side='sell', size = str(sellDat)))
      lastSell =  float(auth_client.get_product_ticker(product_id=currency)['price'])
      
      trdCnt += 1
      sell = False
      buy = True
            
# STEP 12 - Place a market buy order if the onditions are met, then tell me, update soldlast variable,turn buy off and sell on, count the new trade.

    if signal == True and  buySignal == True and buy == True:
      print(auth_client.place_market_order(product_id = currency, side='buy', funds = str(funding)))
      lastBuy =  float(auth_client.get_product_ticker(product_id=currency)['price'])
      
      trdCnt += 1
      sell = True
      buy = False

            
# STEP 13 - Tell me all about everything
    if nerdStats == str( 'YES'):
        print(iteration,
            '|trades:', trdCnt,
            '|bet:', desiredBuy,
            '|price:', price,
            '|ditch:',desiredSell,
            '|had:',startingValue,'|have:',
            currentValue,coin,owned,fiat,funding,'|earned:',
            profit, 'sell:',sell,
            'buy:',buy,
            'decision:',signal)

    if nerdStats == str( 'NO' ):
      print(iteration, profit)
# STEP 14 - Take a few seconds to breathe, then do it again.
    
    time.sleep(15)
