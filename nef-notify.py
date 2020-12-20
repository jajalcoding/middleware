# pip install httpx[http2]
# pip install pyaml
# pip install pysyslogclient
# r = httpx.post('https://httpbin.org/post', data={'key': 'value'})      https://www.python-httpx.org/quickstart/

import httpx
import sys
import yaml
import pysyslogclient
import logging
import pdb

try:
   namafile = sys.argv[1]
except:
    print("Using default file client2nef.yaml... Please enter argument file name if want to use others !")
    namafile = 'nef-notify.yaml'

try:
    f = open(namafile, "r")
except:
    print(namafile+" can not be opened!")
    exit()

logging.basicConfig(filename='nef-notify.log', filemode='a', 
                    format='%(asctime)s - %(message)s', level=logging.INFO)

logging.info('Nef-Notify App started')

sentdata = yaml.load(f, Loader=yaml.FullLoader)
f.close()
logging.info("YAML : "+str(sentdata))

# remove server from data because no need to be posted
targetserver = sentdata['server']
sentdata.pop('server')

# msisdn is array so that multiple msisdn can be subscribed
# after getting it, then pop it out 

try :
   targetmsisdn = sentdata['msisdn']
   sentdata.pop('msisdn')
except:
   print("MSISDN not found - exiting")
   logging.info("MSISDN not found - exiting")
   exit()

# it looks like if http2=True using POST, always there is exception error
# *** h2.exceptions.InvalidBodyLengthError: InvalidBodyLengthError: Expected 15 bytes, received 0
# but it only occurs when going to quart http/2

client = httpx.Client(http2=False, verify=False)

for msisdn in targetmsisdn :
    sentdata['msisdn'] = str(msisdn)
    try:
        logging.info("POST : "+str(sentdata))
        response = client.post(targetserver,json=sentdata)
        logging.info("SERVER: "+response.http_version+" "+str(response.status_code)+" - "+response.text)
        print('POST OK to '+targetserver)
    except:
        print("Can not reach "+targetserver)
        logging.info("SERVER ERROR - Can not reach/post server !")
        exit()

logging.info('Nef-Notify App ended')
print('Nef-Notify App ended..')