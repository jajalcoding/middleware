from flask import Flask,request
import pdb

app = Flask(__name__)

@app.route('/')
def hello():
    return '<html><h1>it works with http2</html>'

@app.route('/one/')
def one():
    print("client accessing one")
    return '<html><h1>ONE</html>'

@app.route('/two/')
def two():
    return '<html><h1>TWO</html>'

@app.route('/login', methods=['GET','POST'])
def login():
    for x in request.form:
        print("    --- "+ x + " : "+request.form[x])
    if request.method == 'POST':
        teks="You are doing a POST"
    else:
        if request.method == 'GET':
            teks="You are doing a GET"
    return teks+"\n"

app.run(
        host='localhost',
        port=8080 )
