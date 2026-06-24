from flask import Flask, jsonify,request

app=Flask(__name__)

@app.route("/api")
def api():
    return "Hello World!"

if "__main__"==__name__:
    app.run(debug=True)
