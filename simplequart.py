from quart import Quart

app = Quart(__name__)

@app.route('/')
async def hello():
    return '<html><h1>it works with http2</html>'

app.run(
        host='localhost',
        port=8080,
        certfile='cert.pem',
        keyfile='privkey.pem',
)
