

import cbpro, datetime, numpy, time
 
##################################################################

currency = input('Please enter the coin you would like to trade: '+ '') + '-USD'

pairA = input('Please confirm your choice'+'')
pairB = 'USD'
##################################################################
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
pairIdA = getAccountId(currency[:3])# Get the currency's specific ID
pairIdB = getAccountId(pairB[:3])# Get the currency's specific ID

def getPrice():
    try:
        productTicker = auth_client.get_product_ticker(product_id=currency)
        currentPrice = float(productTicker['price'])
        return currentPrice
    except:
        print('Something may have gone wrong with credentials or you may have a typo in the coin you chose')





def coppockSignal():

    historicData = auth_client.get_product_historic_rates(currency, granularity=300)
    historicRates = numpy.squeeze(numpy.asarray(numpy.matrix(historicData)[:,4]))
    ROC11 = numpy.zeros(13)
    ROC14 = numpy.zeros(13)
    ROCSUM = numpy.zeros(13)
    for ii in range(0,13):
        ROC11[ii] = (100*(historicRates[ii]-historicRates[ii+11]) / float(historicRates[ii+11]))
        ROC14[ii] = (100*(historicRates[ii]-historicRates[ii+14]) / float(historicRates[ii+14]))
        ROCSUM[ii] = ( ROC11[ii] + ROC14[ii] )
    coppock = numpy.zeros(4)
    for ll in range(0,4):
        coppock[ll] = (((1*ROCSUM[ll+9]) + (2*ROCSUM[ll+8]) + (3*ROCSUM[ll+7]) \
        + (4*ROCSUM[ll+6]) + (5*ROCSUM[ll+5]) + (6*ROCSUM[ll+4]) \
        + (7*ROCSUM[ll+3]) + (8*ROCSUM[ll+2]) + (9*ROCSUM[ll+1]) \
        + (10*ROCSUM[ll])) / float(55))
    coppockD1 = numpy.zeros(3)
    for mm in range(3):
        coppockD1[mm] = coppock[mm] - coppock[mm+1]
    coppockOut = ((coppockD1[0]/abs(coppockD1[0]) , coppockD1[1]/abs(coppockD1[1])))

    if (coppockD1[0]/abs(coppockD1[0])) == -1.0 and (coppockD1[1]/abs(coppockD1[1])) == 1.0:
        signal = True
    else:
        signal = False
    return signal
signal = coppockSignal()

##################################################################

'''productTicker = auth_client.get_product_ticker(product_id=currency)
currentPrice = float(productTicker['price'])'''
currentPrice = float(getPrice())
print(currentPrice)
fee = 0.011
sellingPowerStart  = float(auth_client.get_account(pairIdA)['available'])
buyingPowerStart  = float(auth_client.get_account(pairIdB)['available']) - 1

sellingPower  = float(auth_client.get_account(pairIdA)['available'])
sellValue = float(sellingPower * currentPrice)



bp = float(auth_client.get_account(pairIdB)['available']) 
buyingPower = round(bp-1,2)
buyValue = float(buyingPower/currentPrice)


soldAt = currentPrice + (currentPrice*fee)
boughtAt = currentPrice - (currentPrice*fee)
startPrice = currentPrice


totalValueCrypto = float(buyValue + sellingPower)
totalValueDollar = float(sellValue + buyingPower)

'''print('--------starting balances--------------')
print('Avalabile:', pairA, 'quantity:', sellingPowerStart)
print(pairA, 'Value:', pairA ,sellValue)
print(pairB, 'Balance:', buyingPowerStart)
print(currency,'Price:', startPrice)
print('---------------------------------------', '\n')'''




iteration = 1
tradeCount = 0
trade = True
firstTrade = True
while trade == True:

    totalValueCrypto = float(buyValue + sellingPower)
    totalValueDollar = float(sellValue + buyingPower)

    time.sleep(1)
    sellingPower  = float(auth_client.get_account(pairIdA)['available'])
    bp = float(auth_client.get_account(pairIdB)['available']) - 1
    buyingPower = round(bp-1,2)
    time.sleep(1) 
    now = datetime.datetime.now()
    today = (now.strftime('%m/%d/%y'))
    timestamp = (now.strftime('%H:%M '))
    minimumSellPrice = float(boughtAt + (boughtAt * fee))
    maximumBuyPrice = float(soldAt - (soldAt * fee))
#########################################################################################
    try:
        coppockSignal()
        print(coppockSignal())
    except:
        pass
    
##################################################################
    
##################################################################
    time.sleep(1)

    
    if firstTrade == False and signal == True and trade == True and buyingPower > 10 and currentPrice < maximumBuyPrice:
        buy = True
        funding = float(buyingPower)            
    else:
        buy = False
    if firstTrade == False and signal == True and (sellingPower > 1)  and (currentPrice > minimumSellPrice)  :
        sell = True
        funding = float(sellingPower)
    else: 
        sell = False
                
    if buy == True and sell == False and signal == True and trade == True :
        auth_client.place_market_order(product_id=currency, side='buy', funds=str(funding))

        boughtAt = currentPrice
        print(iteration,'buy!',timestamp, currentPrice, sellingPower, buyingPower)

    if sell == True and buy == False and signal == True and trade == True :
        auth_client.place_market_order(product_id=currency,side='sell',size=str(funding))

        soldAt = currentPrice
        print(iteration,'sell!',timestamp, getPrice(), sellingPower, buyingPower)
        
                        
    if firstTrade == True and (buyingPower > 5) and signal == True and trade == True and (currentPrice < startPrice):
            
        auth_client.place_market_order(product_id=currency, side='buy', funds=str(buyingPower))
        boughtAt = currentPrice
        firstTrade = False

        print(iteration,'buy!',timestamp, currentPrice, sellingPower, buyingPower)
       
    if firstTrade == True and (sellingPower * currentPrice > 5) and signal == True and trade == True and (currentPrice > startPrice):
        auth_client.place_market_order(product_id=currency,side='sell',size=str(sellingPower))
        soldAt = currentPrice
        firstTrade = False

        print(iteration,'sell!',timestamp, currentPrice, sellingPower, buyingPower)
    print(timestamp, firstTrade, signal, '|',buy, sell,'|', getPrice(), sellingPower, buyingPower)

######################################################################################### 
   
    
    iteration = iteration + 1
    
    

    time.sleep(60)
