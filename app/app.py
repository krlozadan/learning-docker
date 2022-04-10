from flask import Flask, render_template
import db

app = Flask(__name__)

@app.route("/")
async def hello_world():
    redis = await db.connect()
    name = await redis.get("name")
    name = "No name found" if name is None else str(name, 'utf-8')
    await redis.close()
    # Use Jinja templating engine
    return render_template("index.html" , name=name)
