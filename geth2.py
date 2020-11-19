# pip install httpx[http2]
# cek with python geth2.py https://www.google.com

import httpx
import sys

 
client = httpx.Client(http2=True)
response = client.get(sys.argv[1])
print(response.text)
print("-----------")
print(response.http_version)