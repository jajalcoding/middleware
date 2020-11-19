# pip install httpx[http2]
# pip install pyaml
# r = httpx.post('https://httpbin.org/post', data={'key': 'value'})      https://www.python-httpx.org/quickstart/
import httpx
import sys
import yaml

try:
   namafile = sys.argv[1]
except:
    print("Need 1 argument, a yaml filename that consist of configuration !")
    exit()

f = open(namafile, "r")
sentdata = yaml.load(f, Loader=yaml.FullLoader)
f.close()
print('From YAML:')
print(sentdata)
print("-------")
print("Waiting for server reply.....")

# remove server from data because no need to be posted
targetserver = sentdata['server']
sentdata.pop('server')

client = httpx.Client(http2=True)
response = client.post(targetserver,data=sentdata)

print(response.text)
print("-----------")
print(response.http_version)
