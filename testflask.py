from flask import Flask

app= Flask(__name__)

@app.route("/")
def testindex():
    return "Hello World --index"

@app.route("/test")
def testapi():
    return "Hello World --test"

if __name__=="__main__":
    app.run()