# pip install quart
# from the pcap, looks like it just return 201 and all parameters are returned back

from quart import Quart,request, make_response
import json
import pdb

app = Quart(__name__)

@app.route('/')
async def hello():
    return '<html><h1>it works with http2</html>'

@app.route('/3gpp-monitoring-event/v1/nef5g/subscriptions', methods=['POST'])
async def subscribe():
    jsondata = (await request.get_json())
    print(jsondata)
    return  { 'result':'ok' }, 201
        

app.run(
        host='localhost',
        port=40880,
        certfile='cert.pem',
        keyfile='privkey.pem',
)
