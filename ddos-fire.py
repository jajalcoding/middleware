# pip install httpx[http2]
# pip install pyaml
# pip install pysyslogclient
# r = httpx.post('https://httpbin.org/post', data={'key': 'value'})      https://www.python-httpx.org/quickstart/

import httpx
import sys
import yaml
import pysyslogclient
import logging
import time
import datetime
from random import randint, shuffle
import pdb

def chosemsisdn(arraymsisdn, number):
    x = list(range(0,number))
    shuffle(x)
    chosen=[]
    for i in range(0,number):
         chosen.append(str(arraymsisdn[x[i]]))
    return chosen


try:
   namafile = sys.argv[1]
except:
    print("Using default file ddos-fire.yaml... Please enter argument file name if want to use others !")
    namafile = 'ddos-fire.yaml'

try:
    f = open(namafile, "r")
except:
    print(namafile+" can not be opened!")
    exit()

logging.basicConfig(filename='ddos-fire.log', filemode='a', 
                    format='%(asctime)s - %(message)s', level=logging.INFO)

logging.info('ddos-fire App started')

sentdata = yaml.load(f, Loader=yaml.FullLoader)
f.close()
logging.info("YAML : "+str(sentdata))

# remove server from data because no need to be posted
targetserver = sentdata['server']
sentdata.pop('server')

# msisdn + period is array so that multiple msisdn can be subscribed
# after getting it, then pop it out 

try :
   targetmsisdn = sentdata['msisdn-ipv4']
   sentdata.pop('msisdn-ipv4')
except:
   print("MSISDN-IPv4 not found - exiting")
   logging.info("MSISDN-IPv4 not found - exiting")
   exit()

# it looks like if http2=True using POST, always there is exception error
# *** h2.exceptions.InvalidBodyLengthError: InvalidBodyLengthError: Expected 15 bytes, received 0
# but it only occurs when going to quart http/2

client = httpx.Client(http2=False, verify=False)

while True:
    noOfmsisdn = randint(10,20)
    chosen = chosemsisdn(targetmsisdn, noOfmsisdn)
    logging.info("Random "+str(noOfmsisdn)+" number :"+str(chosen))

    for msisdn in chosen:
        sentdata['monitoringEventReports'][0]['msisdn'] = str(msisdn)
        sentdata['monitoringEventReports'][0]['eventTime'] = datetime.datetime.now().astimezone().strftime("%Y-%m-%dT%H:%M:%S %z")
# parse ip address = last 8 char        
        sentdata['monitoringEventReports'][0]['pdnConnInfo']['ipv4Addr'] = msisdn[8:10]+'.'+msisdn[10:12]+'.'+msisdn[12:14]+'.'+msisdn[14:16]
        try:
            logging.info("POST : "+str(sentdata))
            response = client.post(targetserver,json=sentdata)
            logging.info("SERVER: "+response.http_version+" "+str(response.status_code)+" - "+response.text)
            print('POST OK to '+targetserver)
        except:
            print("Can not reach "+targetserver)
            logging.info("SERVER ERROR - Can not reach/post server !")
            exit()
        time.sleep(randint(20,90)/100)
        print(sentdata)
# random time between ddos event fire ( 60-180 seconds )
    time.sleep(randint(60,180))

logging.info('ddos-fire App ended')
print('ddos-fire ended..')
