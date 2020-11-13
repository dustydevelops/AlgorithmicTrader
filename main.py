import cbpro, time, numpy as np
from apiShit import auth_client


#  Pick a pair to trade

coin = input('      Enter coin (xtz recommended):'+'').upper()
fiat = input('      Enter native currency:'+'').upper()
currency = (coin+'-'+fiat)
granularity = input('      granularity (60,300,900,3600):'+'')
gran = int(granularity)
nerdStats = input('      NerdStats? yes or no:'+'').upper()

#  Get the ID's for the chosen pair 

def account(iD):
 for account in auth_client.get_accounts():
  if account['currency'] == iD:
   return account['id']
  
def lastFillPrice():
 fills_gen = auth_client.get_fills(currency)
 all_fills = list(fills_gen)
 fill = (all_fills[0]['price'])
 return fill

def lastFillSide():
 fills_gen = auth_client.get_fills(currency)
 all_fills = list(fills_gen)
 i = (all_fills[0][ 'side'] == 'buy')
 if i == True:
  side = 'Bought'
 elif i == False:
   side = 'Sold'
 return side
time.sleep(1)
# Get the chosen pair's current price
startingPrice = float(auth_client.get_product_ticker(product_id=currency)['price'])

# Get the chosen pair's current balances
startingCoin = float(auth_client.get_account(account(coin[:3]))['available'])
startingDollar = float(auth_client.get_account(account(fiat[:3]))['available'])
startingValue = float(startingDollar + (startingCoin * startingPrice))

#  Set the prices to later distinguish high from low and make profitable trades.

lastBuy = float(lastFillPrice())
lastSell = float(lastFillPrice())
# we start looking to buy
if lastFillSide() == 'Sold':
  buy = True
  sell = False
if lastFillSide() == 'Bought':
  buy = False
  sell = True


#  Iinitaite the loop, start iteration count, and trade count, begin loop.

trdCnt = 0
iteration = 0
try:
  trade = True
  while trade == True:
    
      iteration += 1
      fee = (0.013)
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
      

      historicData = auth_client.get_product_historic_rates(currency, granularity=gran)

        # Make an array of the historic price data from the matrix
      p = np.squeeze(np.asarray(np.matrix(historicData)[:,4]))

        # Wait for 1 second, to avoid API limit
      time.sleep(3)
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
        if sellSignal == True and sell == True:
          print(auth_client.place_market_order(product_id = currency, side='sell', size = str(sellDat)))
          lastSell =  float(auth_client.get_product_ticker(product_id=currency)['price'])
          trdCnt += 1
          sell = False
          buy = True
          time.sleep(30)
        
        if buySignal == True and buy == True:
          print(auth_client.place_market_order(product_id = currency, side='buy', funds = str(funding)))
          lastBuy =  float(auth_client.get_product_ticker(product_id=currency)['price'])
          trdCnt += 1
          sell = True
          buy = False
          time.sleep(30)
        
      else:
      
        signal = False
        if nerdStats == str( 'YES'):
            print('\n',iteration,
                'trades:', trdCnt,
                '|bet:', desiredBuy,
                '|price:', price,
                '|ditch:',desiredSell,
                '|had:',startingValue,
                '|have:',currentValue,
                '|earned:',profit,
                '|balances:',coin,owned,fiat,funding,
                '|decision making: buy-', buy,
                'sell-',sell,'execute-',signal,'\n')

        if nerdStats == str( 'NO' ):
          continue

  time.sleep(15)

except Exception as e:
   print(e)
