

import cbpro, datetime, numpy, time
 

currency = input('Please enter the coin you would like to trade: '+ '') + '-USD'

pairA = input('Please confirm your choice'+'')
pairB = 'USD'

def authorized():
   apiKey = 'your api key here'
   apiSecret = 'your api secret here'
   passphrase = 'passphrase goes here'
    auth_client = cbpro.AuthenticatedClient(apiKey,apiSecret,passphrase)
    return auth_client
auth_client = authorized()

def getAccountId(cur):
   x = auth_client.get_accounts()
   for account in x:
    if account['currency'] == cur:
     return account['id']
    
def getBuyPower():
    bp = float(auth_client.get_account(pairIdB)['available']) 
    buyingPower = round(bp-1,2)
    return buyingPower

def getPrice():

    productTicker = auth_client.get_product_ticker(product_id=currency)
    currentPrice = float(productTicker['price'])
    return currentPrice
def determineConditions():

    coinToDollar = getPrice * sellingPower
    dollarToCoin = valueC = buyingValue/getPrice
        
    
    print(coinToDollar,dollarToCoin)

def determineBuy():
    if getPrice() < startPrice:
        buy = True
    else:
        buy = False
    return buy

def determineSell():
    if getPrice() > startPrice:
        sell = True
    else:
        sell = False
    return sell


    

currency = input('Please enter the coin you would like to trade: '+ '') + '-USD'
pairA = input('Please enter your coin choice again to confirm: '+'')
pairB = 'USD'

auth_client = authorized()

startPrice = getPrice()
currentPrice = getPrice()

pairIdA = getAccountId(currency[:3])# Get the currency's specific ID
pairIdB = getAccountId(pairB[:3])# Get the currency's specific ID


buyingPower = getBuyPower()



fee = 0.011

sellingPowerStart  = float(auth_client.get_account(pairIdA)['available'])
buyingPowerStart  = float(auth_client.get_account(pairIdB)['available']) - 1

sellingPower  = float(auth_client.get_account(pairIdA)['available'])
sellValue = float(sellingPower * currentPrice)




buyValue = float(buyingPower/currentPrice)


soldAt = currentPrice + (currentPrice*fee)
boughtAt = currentPrice - (currentPrice*fee)
startPrice = currentPrice
tradeCount = 0
iteration = 1


trade = True
firstTrade = True
while trade == True:

    totalValueCrypto = float(buyValue + sellingPower)
    totalValueDollar = float(sellValue + buyingPower)
    sellingPower  = float(auth_client.get_account(pairIdA)['available'])


    
    time.sleep(1) 
    now = datetime.datetime.now()
    today = (now.strftime('%m/%d/%y'))
    timestamp = (now.strftime('%H:%M '))
    minimumSellPrice = float(boughtAt + (boughtAt * fee))
    maximumBuyPrice = float(soldAt - (soldAt * fee))
    sell = determineSell()
    
            

  
    candle = 300
    historicData = auth_client.get_product_historic_rates(currency, granularity=candle)
    historicRates = numpy.squeeze(numpy.asarray(numpy.matrix(historicData)[:,4]))

# Use the 11th and 14th price back to calculate rate of change. they all = numpy.zeoros(13) but they are not the same. do not alter.
    ROC11 = numpy.zeros(13)
    ROC14 = numpy.zeros(13)
    ROCSUM = numpy.zeros(13)
        
    for ii in range(0,13):
        ROC11[ii] = (100*(historicRates[ii]-historicRates[ii+11]) / float(historicRates[ii+11]))
        ROC14[ii] = (100*(historicRates[ii]-historicRates[ii+14]) / float(historicRates[ii+14]))
        ROCSUM[ii] = ( ROC11[ii] + ROC14[ii] )
# Calculate the past 4 values from coppock using a weighted moving Average.

        time.sleep(1)
    coppock = numpy.zeros(4)
    for ll in range(0,4):
        coppock[ll] = (((1*ROCSUM[ll+9]) + (2*ROCSUM[ll+8]) + (3*ROCSUM[ll+7]) \
        + (4*ROCSUM[ll+6]) + (5*ROCSUM[ll+5]) + (6*ROCSUM[ll+4]) \
        + (7*ROCSUM[ll+3]) + (8*ROCSUM[ll+2]) + (9*ROCSUM[ll+1]) \
        + (10*ROCSUM[ll])) / float(55))
# Calculate last 3 derivatives from coppock.
    coppockD1 = numpy.zeros(3)
    for mm in range(3):
        coppockD1[mm] = coppock[mm] - coppock[mm+1]
    if (coppockD1[0]/abs(coppockD1[0])) == -1.0 and (coppockD1[1]/abs(coppockD1[1])) == 1.0:
        signal = True

    else:
        signal = False
  



    if determineBuy() == True and sell == False and signal == True and trade == True :
        #auth_client.place_market_order(product_id=currency, side='buy', funds=str(funding))

        boughtAt = currentPrice
        print(iteration,'buy!',timestamp, currentPrice, sellingPower, buyingPower)
        firstTrade = False
        
    if sell == True and determineBuy() == False and signal == True and trade == True :
        #auth_client.place_market_order(product_id=currency,side='sell',size=str(funding))

        soldAt = currentPrice
        print(iteration,'sell!',timestamp, getPrice(), sellingPower, buyingPower)
        firstTrade = False

    print(iteration,'firstTrade:', firstTrade, 'signal :', signal,'determineBuy():',determineBuy(),'determineSell() :',determineSell(),'startPrice:', startPrice, 'getPrice:', getPrice(),'sellingPower', sellingPower,'buyingPower', buyingPower)

    iteration = iteration + 1
    
    

    time.sleep(30)

