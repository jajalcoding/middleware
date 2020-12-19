# pip install quart

from quart import Quart,request, make_response
import pdb

app = Quart(__name__)

@app.route('/')
async def hello():
    return '<html><h1>it works with http2</html>'

@app.route('/one/')
async def one():
    print("client accessing one")
    return '<html><h1>ONE</html>'

@app.route('/two/')
async def two():
    return '<html><h1>TWO</html>'

@app.route('/login', methods=['GET','POST'])
async def login():
    formdata = await ( request.form )
    print(formdata)
    if request.method == 'POST':
        teks="You are doing a POST"
    else:
        if request.method == 'GET':
            teks="You are doing a GET"
    return teks+" "+formdata['name']

@app.route('/json', methods=['POST'])
async def jsontest():
    formdata = await ( request.form )
    print(formdata)
    return { 'city': 'jakarta', 'country':'indonesia'}

@app.route('/test201', methods=['POST'])
async def test201():
    formdata = await ( request.form )
    print(formdata)
    return  { 'result': 'All Good', 'number':'303' }, 201
        

app.run(
        host='localhost',
        port=8080,
        certfile='cert.pem',
        keyfile='privkey.pem',
)

'''
curl https://localhost:8080/test201 -k -v -d "name=teguh" -d "alamat=jakarta"

HTTP/2 201
< content-type: application/json
< content-length: 36
< date: Sat, 19 Dec 2020 09:24:12 GMT
< server: hypercorn-h2
<
* Connection #0 to host localhost left intact
{"number":"303","result":"All Good"}*


'''
