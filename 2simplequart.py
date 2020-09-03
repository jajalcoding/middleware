from quart import Quart

app = Quart(__name__)

@app.route('/')
async def hello():
    return '<html><h1>it works with http2</html>'

@app.route('/one/')
async def one():
    return '<html><h1>ONE</html>'

@app.route('/two/')
async def two():
    return '<html><h1>TWO</html>'

app.run(
        host='localhost',
        port=8080,
        certfile='cert.pem',
        keyfile='privkey.pem',
)
