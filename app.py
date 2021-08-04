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
    # search query 확인하기
    search_text = request.args.get('text', "")
    search_abv = request.args.get('abv_lv')
    abv_obj = {
        "1": {"checked": False, "text": "0.0% ~ 1.9%", 'gte': 0, "lt": 2},
        "2": {"checked": False, "text": "2.0% ~ 3.9%", 'gte': 2, "lt": 4},
        "3": {"checked": False, "text": "4.0% ~ 5.9%", 'gte': 4, "lt": 6},
        "4": {"checked": False, "text": "6.0% ~ 7.9%", 'gte': 6, "lt": 8},
        "5": {"checked": False, "text": "8.0% ~ ", 'gte': 8, "lt": 999},
    }
    # $match 구성
    match_info = {}
    if search_text is not None:
        match_info["name"] = { "$regex": search_text }
    if search_abv is not None:
        search_abv = search_abv.split(",")
        match_info["$or"] = []
        for key in search_abv:
            if key not in abv_obj: continue
            abv_obj[key]["checked"] = True
            match_info["$or"].append({"abv": { "$gte": abv_obj[key]["gte"], "$lt": abv_obj[key]["lt"] }})
        if len(match_info["$or"]) < 1:
            match_info.pop("$or", None)
    # TODO: aggregate로 review sorting하기
    beers = db.beers.aggregate([
                {"$match": match_info},
                {"$lookup": {"from": "reviews", "localField": "_id", "foreignField": "beer_id", "as": "reviews"}},
            ])
    beers = list(beers)
    # beer에 reviewCount 추가 등 조작
    for beer in beers:
        beer["_id"] = str(beer["_id"])
        beer["reviewCount"] = len(beer["reviews"])
        if len(beer["reviews"]) > 0:
             beer["reviews"] = sorted(beer["reviews"], reverse=True, key=lambda review: review.get("created_at"))

    if username is None:
        return render_template("index.html", beersList=beers, search_text=search_text, abv_obj=abv_obj)
    else:
        return render_template("index.html", beersList=beers,search_text=search_text, abv_obj=abv_obj, username=username)

@app.route("/beer/<_id>")
@jwt_required(optional=True)
def show_beer(_id):
    try:
        username = get_jwt_identity()
        beer = db.beers.find_one({"_id": ObjectId(_id)})
        reviews = db.reviews.find({"beer_id": ObjectId(_id)}).sort([("created_at", -1)])
        reviews = list(reviews)
        for review in reviews:
            review["_id"] = str(review["_id"])
            review["beer_id"] = str(review["beer_id"])
        if username is None:
            return render_template("detail.html", beer=beer, reviews=reviews)
        else:
            return render_template("detail.html", beer=beer, reviews=reviews, username=username)
    except Exception as e:
        print("[Error] Detail Page", e)
        return redirect(url_for('main'))


#### #### #### #### ####
#### #### API  #### ####
#### #### #### #### ####
app.register_blueprint(routes)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
