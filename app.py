from flask import Flask, render_template, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

import xml.etree.ElementTree as elemTree

# parse XML
try:
    tree = elemTree.parse("keys.xml")
    SECRET_KEY = tree.find('string[@name="AUTH_SECRET_KEY"]').text
    MONGO_DB_URL = tree.find('string[@name="MONGO_DB_URL"]').text
except:
    print("ERROR!!! check your 'keys.xml' file")
    SECRET_KEY = "jungle1234"
    MONGO_DB_URL = "localhost"

# print("** SECRET_KEY **", SECRET_KEY)
# print("** MONGO_DB_URL **", MONGO_DB_URL)

app = Flask(__name__)
client = MongoClient(MONGO_DB_URL, 27017)
db = client.beerdb


@app.route("/")
def main():
    beers = db.beers.find({})
    beers = list(beers)
    for beer in beers:
        beer["_id"] = str(beer["_id"])
    return render_template("index.html", beersList=beers)


@app.route("/beer/<id>")
def show_beer(id):
    try:
        beer = db.beers.find_one({"_id": ObjectId(id)})
        return render_template("detail.html", beer=beer)
    except Exception as e:
        return redirect(url_for('main'))

#### #### #### #### ####
#### #### API  #### ####
#### #### #### #### ####
from routes import *
app.register_blueprint(routes)






if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
