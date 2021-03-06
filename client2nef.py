# pip install httpx[http2]
# pip install pyaml
# pip install pysyslogclient
# r = httpx.post('https://httpbin.org/post', data={'key': 'value'})      https://www.python-httpx.org/quickstart/
# 

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
    namafile = 'client2nef.yaml'

#SERVER = "202.55.91.162"
#PORT = 10514

try:
    f = open(namafile, "r")
except:
    print(namafile+" can not be opened!")
    exit()

logging.basicConfig(filename='client2nef.log', filemode='a', 
                    format='%(asctime)s - %(message)s', level=logging.INFO)

logging.info('Client2Nef App started')

sentdata = yaml.load(f, Loader=yaml.FullLoader)
f.close()
logging.info("YAML : "+str(sentdata))
#print('From YAML:')
#print(sentdata)
#print("-------")
#print("Waiting for server reply.....")

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

client = httpx.Client(http2=True, verify=False)

for msisdn in targetmsisdn :
    sentdata['msisdn'] = str(msisdn)
    try:
        logging.info("POST : "+str(sentdata))
        response = client.post(targetserver,json=sentdata)
        print(response.text)
        logging.info("SERVER: "+response.http_version+" "+str(response.status_code)+" - "+response.text)
    except:
        print("Can not reach "+targetserver)
        logging.info("SERVER ERROR - Can not reach/post server !")
        exit()

logging.info('Client2Nef App ended')
exit()


# no need syslog for this test

print("Sending to SYSLOG "+SERVER+":"+str(PORT)+"....")
client = pysyslogclient.SyslogClientRFC5424(SERVER, PORT, proto="TCP")
client.maxMessageLength = 6000

# need to add error handling here - can not find a way how to error handling this module :(

client.log(response.text,
	facility=pysyslogclient.FAC_SYSTEM,
	severity=pysyslogclient.SEV_EMERGENCY,
	program="Logger",
	pid=1)

client.close()
