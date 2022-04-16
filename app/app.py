from flask import Flask, request
from db import get_name, set_name

app = Flask(__name__)

@app.route("/")
async def hello_world():
    return app.send_static_file('index.html')

@app.route("/name", methods=["GET", "POST"])
async def name():
    if request.method == "GET":
        return await get_name()
    else:
        new_name = request.get_json()["name"]
        await set_name(new_name)
        return new_name