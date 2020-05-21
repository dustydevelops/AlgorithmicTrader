

import cbpro, datetime, numpy, time
 
def authorized():
   apiKey = 'your api key here'
   apiSecret = 'your api secret here'
   passphrase = 'passphrase goes here'
    auth_client = cbpro.AuthenticatedClient(apiKey,apiSecret,passphrase)
    return auth_client

tradeCount = 0
iteration = 1

def getCurrencyInput():
   x = input('Please enter the coin you would like to trade: '+ '') + '-USD'
   return x
currency = getCurrencyInput()

def getAccountId(cur):
   x = auth_client.get_accounts()
   for account in x:
    if account['currency'] == cur:
     return account['id']
pairIdA = getAccountId(currency[:3])# Get the currency's specific ID
pairIdB = getAccountId('USD'[:3])# Get the currency's specific ID

def getBuyPower():
    bp = float(auth_client.get_account(pairIdB)['available']) 
    buyingPower = round(bp-1,2)
    return buyingPower

def getSellPower():
    sellingPower = float(auth_client.get_account(pairIdA)['available'])
    return sellingPower
    

def getPrice():
    productTicker = auth_client.get_product_ticker(product_id=currency)
    currentPrice = float(productTicker['price'])
    return currentPrice


def determineBuy():
    if firstTrade == True and (getPrice() < startPrice) == True:
        buy = True
    else:

        if firstTrade == False and (getPrice() < (lastSell - (lastSell * 0.005))) == True:
            buy = True
        else:
            buy = False
    return buy


def determineSell():
    if firstTrade == True and (getPrice() > startPrice) == True:
        sell = True
    else:
        if firstTrade == False and (getPrice() > (lastBuy + (lastBuy * 0.005))) == True:
            sell = True
        else:
            sell = False
    return sell


def getCoppockSignal():
    candle = 300
    historicData = auth_client.get_product_historic_rates(currency, granularity=candle)
    historicRates = numpy.squeeze(numpy.asarray(numpy.matrix(historicData)[:,4]))
    ROC11 = numpy.zeros(13)
    ROC14 = numpy.zeros(13)
    ROCSUM = numpy.zeros(13)       
    for ii in range(0,13):
        ROC11[ii] = (100*(historicRates[ii]-historicRates[ii+11]) / float(historicRates[ii+11]))
        ROC14[ii] = (100*(historicRates[ii]-historicRates[ii+14]) / float(historicRates[ii+14]))
        ROCSUM[ii] = ( ROC11[ii] + ROC14[ii] )

        time.sleep(1)
    coppock = numpy.zeros(4)
    for ll in range(0,4):
        coppock[ll] = (((1*ROCSUM[ll+9]) + (2*ROCSUM[ll+8]) + (3*ROCSUM[ll+7]) \
        + (4*ROCSUM[ll+6]) + (5*ROCSUM[ll+5]) + (6*ROCSUM[ll+4]) \
        + (7*ROCSUM[ll+3]) + (8*ROCSUM[ll+2]) + (9*ROCSUM[ll+1]) \
        + (10*ROCSUM[ll])) / float(55))

    coppockD1 = numpy.zeros(3)
    for mm in range(3):
        coppockD1[mm] = coppock[mm] - coppock[mm+1]
    if (coppockD1[0]/abs(coppockD1[0])) == -1.0 and (coppockD1[1]/abs(coppockD1[1])) == 1.0:
        signal = True

    else:
        signal = False
    return signal


startPrice = getPrice()

sellingPowerStart  = getSellPower()
buyingPowerStart  = getBuyPower()
lastBuy = getPrice()


trade = True
firstTrade = True

while trade == True:

    buyingPower = getBuyPower()
    sellingPower  = getSellPower()  

    now = datetime.datetime.now()
    today = (now.strftime('%m/%d/%y'))
    timestamp = (now.strftime('%H:%M '))


    if determineBuy() == True and getCoppockSignal() == True :
        #auth_client.place_market_order(product_id=currency, side='buy', funds=str(funding))
        print(iteration,'buy!',timestamp, lastBuy, sellingPower, buyingPower)

        lastBuy = getPrice()
        firstTrade = False
    
        
        
    if determineSell() == True and getCoppockSignal() == True :
        #auth_client.place_market_order(product_id=currency,side='sell',size=str(funding))
        firstTrade = False

        lastSell = getPrice()
        print(iteration,'sell!',timestamp, lastSell, float(sellingPower), buyingPower)
    print(iteration,'firstTrade:', firstTrade, 'signal :',getCoppockSignal(),'determineBuy():',determineBuy(),'determineSell() :',determineSell(),'startPrice:', startPrice, 'getPrice:', getPrice(),'sellingPower', sellingPower,'buyingPower', buyingPower)

    
    iteration = iteration + 1
    time.sleep(30)
