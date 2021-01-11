# pip install quart
# from the pcap, looks like it just return 201 and all parameters are returned back
# module /notifyme and /ddosnotify

from quart import Quart,request, make_response
import json
import pysyslogclient
import time
import pdb
import logging

def sendsyslog(teks):
    SERVER = "34.101.221.107"
    PORT = 21212
    print("Sending to SYSLOG "+SERVER+":"+str(PORT)+"....")
    client = pysyslogclient.SyslogClientRFC5424(SERVER, PORT, proto="TCP")
    client.maxMessageLength = 6000
    # need to add error handling here - can not find a way how to error handling this module :(
    client.log(teks,
        facility=pysyslogclient.FAC_SYSTEM,
        severity=pysyslogclient.SEV_EMERGENCY,
        program="Logger",
        pid=1)
    client.close()

logging.basicConfig(filename='client-listen.log', filemode='a', 
                    format='%(asctime)s - %(message)s', level=logging.INFO)
logging.info('Client-Listen.py App started')

app = Quart(__name__)

@app.route('/')
async def hello():
    return '<html><h1>it works</html>'

@app.route('/notifyme', methods=['POST'])
async def subscribe():
    jsondata = (await request.get_json())
    print(jsondata)
    logging.info('POSTED :'+str(jsondata))
# this procedure contains a blocking ( non-async ), so if tcp connection to syslog is bad
# it will halt other connection... this is at the moment is unresolvable, until there is a syslog client
# module that can support asyncio !
    sendsyslog(str(jsondata))
    return { 'result':'ok' }, 204

@app.route('/ddosnotify', methods=['POST'])
async def ddosnotify():
    jsondata = (await request.get_json())
    print(jsondata)
    logging.info('POSTED :'+str(jsondata))
    sendsyslog(str(jsondata))
    return { 'result':'ok' }, 204

app.run(
        host='localhost',
        port=50880,
        certfile='cert.pem',
        keyfile='privkey.pem',
)

logging.info('Client-Listen.py App STOP')
