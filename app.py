<<<<<<< HEAD
from routes import *
from flask import Flask, render_template, redirect, url_for
=======
from flask import Flask, render_template, redirect, url_for, make_response
from flask_wtf.csrf import CSRFProtect
>>>>>>> johnny_jwt-rebuild
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
			DEBUG = True,
			JWT_SECRET_KEY = SECRET_KEY
		)

# JWT 확장 모듈을 flask 어플리케이션에 등록
jwt = JWTManager(app)

# JWT 쿠키 저장
app.config['JWT_COOKIE_SECURE'] = False  # https를 통해서만 cookie가 갈 수 있는지 (production 에선 True)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_ACCESS_COOKIE_PATH'] = '/'  # access cookie를 보관할 url (Frontend 기준)
app.config['JWT_REFRESH_COOKIE_PATH'] = '/'  # refresh cookie를 보관할 url (Frontend 기준)
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
        beers = db.beers.find({})
        beers = list(beers)
        for beer in beers:
            beer["_id"] = str(beer["_id"])
        return render_template("index.html", beersList=beers, username=username)


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
app.register_blueprint(routes)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
