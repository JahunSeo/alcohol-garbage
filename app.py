from routes import *
from flask import Flask, render_template, redirect, url_for
# from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient
from bson.objectid import ObjectId

from flask_jwt_extended import *
import datetime
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


# 토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
app.config.update(
    DEBUG=True,
    JWT_SECRET_KEY=SECRET_KEY
)

# JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(app)

# JWT 쿠키 저장
# https를 통해서만 cookie가 갈 수 있는지 (production 에선 True)
app.config['JWT_COOKIE_SECURE'] = False
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
# access cookie를 보관할 url (Frontend 기준)
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
# refresh cookie를 보관할 url (Frontend 기준)
app.config['JWT_REFRESH_COOKIE_PATH'] = '/'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(seconds=3600)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = datetime.timedelta(seconds=3600)


@app.route("/")
@jwt_required(optional=True)
def main():
    username = get_jwt_identity()
    if username is None:
        beers = db.beers.find({})
        beers = list(beers)
        for beer in beers:
            beer["_id"] = str(beer["_id"])
        return render_template("index.html", beersList=beers)
    else:
        beers = db.beers.find({})  # TODO: join reviews
        beers = list(beers)
        for beer in beers:
            beer["_id"] = str(beer["_id"])
        return render_template("index.html", beersList=beers, username=username)


@app.route("/beer/<_id>")
@jwt_required(optional=True)
def show_beer(_id):
    try:
        username = get_jwt_identity()
        beer = db.beers.find_one({"_id": ObjectId(_id)})
        reviews = db.reviews.find({"beer_id": _id})
        reviews = list(reviews)
        for review in reviews:
            review["_id"] = str(review["_id"])
            review["beer_id"] = str(review["beer_id"])
        if username is None:
            return render_template("detail.html", beer=beer, reviews=reviews )
        else:
            return render_template("detail.html", beer=beer, reviews=reviews, username=username)
    except Exception as e:
        return redirect(url_for('main'))


#### #### #### #### ####
#### #### API  #### ####
#### #### #### #### ####
app.register_blueprint(routes)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
