import cbpro, time, numpy
from twilio.rest import Client

  
key = ''
secret =''
phrase =''
phoneNumber = '+1801'

auth = cbpro.AuthenticatedClient(key,secret,phrase)
sext = Client('aC95e0d822dbfa00bd7cc02a3af83f23d4','e9803226b97bf4e50d6e84e9dcc60898')

def account(iD):
 for account in auth.get_accounts():
  if account['currency'] == iD:
   return account['id']
def approval():
 while True:
   try:
     print('  owned:',owned)
     time.sleep(.5)
   
     print('   last',fill[ 'side'],':',fillPrice)
     if fill['side'] == 'sell':
       print ('    looking to: buy')
     
     time.sleep(.5)
     if fill['side'] == 'buy':
       print ('    looking to: sell')
       
     if fill['side'] == 'buy': print('     estimated gain:',round(owned*price-owned*fillPrice,2) ),time.sleep(.5)

     if fill[ 'side'] == 'buy' and price > fillPrice * 1.02:
          approval = 'sell'
          print('     is in a profitable selling range ')
     elif fill[ 'side'] == 'sell' and price < (fillPrice - (fillPrice * 0.02)):
          approval = 'buy'
          print('     is in a profitable buying range ')
     elif fill[ 'side'] == 'buy' and price < (fillPrice - (fillPrice * 0.099)):
          approval = 'stop loss'
          print('     is dangerously low!')
     elif fill[ 'side'] == 'sell' and price > (fillPrice + (fillPrice * 0.5)):
          approval = 're-up'
          print('      re-up')
     else:
       
       if fill[ 'side'] == 'buy': print('     price too low:', round((fillPrice * 1.02)-price,4)),time.sleep(.5)

       if fill[ 'side'] == 'sell': print('    price too high:',round(price - (fillPrice - (fillPrice * 0.012)),4)),time.sleep(.5)
       
       approval = None

      
     return approval
   except Exception as e:
      print('approval error',e)
 
def signal():
 if permission == None:
   signal = None
  
 else:
  try:
   hd = auth.get_product_historic_rates(currency, granularity=300)
   p = numpy.squeeze(numpy.asarray(numpy.matrix(hd)[:,4]))
   ROC11 = numpy.zeros(13)
   ROC14 = numpy.zeros(13)
   ROCSUM = numpy.zeros(13)
   for ii in range(0,13):
    ROC11[ii] = (100*(p[ii]-p[ii+11]) / float(p[ii+11]))
    ROC14[ii] = (100*(p[ii]-p[ii+14]) / float(p[ii+14]))
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
   signal = ((coppockD1[0]/abs(coppockD1[0])) == 1.0 and (coppockD1[1]/abs(coppockD1[1])) == -1.0)
   if permission == 'sell': permi = 'sell'
   if permission == 'buy': permi = 'buy'
   print('      prediction:',((coppockD1[0]/abs(coppockD1[0])),(coppockD1[1]/abs(coppockD1[1]))))
   return signal
  except Exception as e:
    print('-----------------signal error:',e )
    
def buy():
    print('     buy',volume,'worth @',price)
    sext.messages.create(from_='+14029238218',to=phoneNumber,body=(str(auth.place_market_order(product_id = str(currency), side='buy',funds = str(volume)))))
    return
  
def sell():
  
    print('     sell',size,'@',price)
    sext.messages.create(from_='+14029238218',to=phoneNumber,body=(str(auth.place_market_order(product_id = str(currency), side='sell', size = str(size)))))
    return
  
def panicSell():
    print(auth.place_market_order(product_id = str(currency), side='sell', size = str(size)))
    time.sleep(5)
    sext.messages.create(from_='+14029238218',to= phoneNumber,body=(str(currency)+' stop loss '+str(size)+' @ '+str(price)))
    return
def reup():
    volume = 33.33
    print('    buy',volume,'worth @',price)
    sext.messages.create(from_='+14029238218',to=phoneNumber,body=(str(auth.place_market_order(product_id = str(currency), side='buy',funds = str(volume)))))
    print('     text message sent to', phoneNumber)
t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
coins = ['YFI','ZEC','BAL','REN','UNI','BTC','UMA',
         'ETH','LRC','BCH','XLM','NMR','LTC','EOS',
         'OXT','XTZ','ETC','REP','MKR','ZRX','XRP',
         'ETC','KNC','OMG','FIL'] 
assets = 24
coin = 0

iteration = 1.0

while True:
 try:

  currency = (coins[coin]+'-'+'USD')
  t = time.localtime()
  current_time = time.strftime("%H:%M:%S", t)
  print('   --------')
  time.sleep(.5)
  print('  iteration:',iteration)
  time.sleep(1)
  print(' time:',current_time)
  

  if coin == assets:

    coin = 0
    
    iteration = round(iteration+1,0)
    

  else:
    specificID = account(currency[:3])
    owned = float(auth.get_account(specificID)['available'])
    size = round(owned*0.5,4)

    if coins[coin] == 'BAL': size = 2.17
    if coins[coin] == 'BCH': size = .125
    if coins[coin] == 'BTC': size = 0.0018
    if coins[coin] == 'EOS': size = 76
    if coins[coin] == 'ETH': size = 0.0599
    
    if coins[coin] == 'ETC': size = 5
    if coins[coin] == 'FIL': size = 1
    if coins[coin] == 'KNC': size = 50
    if coins[coin] == 'LRC': size = 180

    if coins[coin] == 'LTC': size = 0.4
    if coins[coin] == 'MKR': size = 0.210
    
    if coins[coin] == 'NMR': size = 1.5
    if coins[coin] == 'OXT': size = 130
    if coins[coin] == 'OMG': size = 10
    if coins[coin] == 'REP': size = 3.8
    if coins[coin] == 'REN': size = 120
    
    if coins[coin] == 'UMA': size = 7.072
    if coins[coin] == 'XLM': size = 200
    if coins[coin] == 'XRP': size = 56
    if coins[coin] == 'XTZ': size = 16
    if coins[coin] == 'YFI': size = 0.0013
    
    if coins[coin] == 'ZEC': size = 0.48
    if coins[coin] == 'ZRX': size = 89
    
    time.sleep(.5)
    print(currency, size)
    price = float(auth.get_product_ticker(product_id=(coins[coin]+'-'+'USD'))['price'])
    time.sleep(.5)
    print(' price:',price)
    fills = list(auth.get_fills(currency))
    virgin = (fills == [])
    if virgin == True:
      volume = 33.33
      buy()
      time.sleep(6)
      fills = list(auth.get_fills(currency))
    fill = fills[0]
    fillPrice = float(fill['price'])
    fund = float(fill['usd_volume'])
    volume = round(fund - (fund * 0.001),2)

    if volume < 33.33: volume = 33.33



    time.sleep(.5)
   
    side = (fill[ 'side'])
    permission = approval()
  
    if permission == 'buy':
       execution = signal() 
       time.sleep(.5)
       if execution == True:
        buy()
    if permission == 'sell':
      execution = signal()
      if execution == True:
       sell()      
    if permission == 'stop loss':
       panicSell()
    if permission == 're-up':
       time.sleep(.5)

       print('   looking to re-up')
       reup()
    
    iteration = round(iteration+0.01,2)
    coin = coin+1
 except Exception as e:
   print(e)
   time.sleep(2)
   
