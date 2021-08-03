from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
import jwt
import bcrypt

import xml.etree.ElementTree as elemTree

# parse XML
try:
   tree = elemTree.parse("keys.xml")
   SECRET_KEY = tree.find('string[@name="AUTH_SECRET_KEY"]').text
   MONGO_DB_URL = tree.find('string[@name="MONGO_DB_URL"]').text
except:
   print("ERROR!!! check your 'keys.xml' file")
   SECRET_KEY = "test1234"
   MONGO_DB_URL = "localhost"

# print("** SECRET_KEY **", SECRET_KEY)
# print("** MONGO_DB_URL **", MONGO_DB_URL)
MONGO_DB_URL = "localhost"

app = Flask(__name__)
client = MongoClient(MONGO_DB_URL, 27017)
db = client.beerdb


@app.route("/api/beer/get", methods=["GET"])
def get_beer():
   # params에서 맥주 아이디 체크
   # 로그인이 되어 있는 경우, 평가 정보 join
   # 다른 사람들의 평가 시간 순 정렬
   beer = {}
   return jsonify({"status": 200, "msg": "맥주 정보 불러오기 성공", "beer": beer})

@app.route("/api/beer/list")
def get_beer_list():
   # 로그인되어 있는 경우, 각 맥주들에 대한 평가 정보 join
   beers = db.beers.find({}).sort([("created_at", -1)])
   return jsonify({"status": 200, "msg": "맥주 리스트 불러오기 성공", "beers": beers})


@app.route("/api/beer/add", methods=["POST"])
def add_beer():
   try:
      # 데이터 확인하기
      formdata = request.get_json()
      formdata = request.form # temp
      name = formdata.get("name")
      abv = formdata.get("abv")
      country = formdata.get("country")
      manufacturer = formdata.get("manufacturer")
      beertype = formdata.get("beertype")
      if not name:
         raise Exception("맥주 이름이 없습니다.")
      if not abv:
         raise Exception("맥주 도수가 없습니다.")
      # 저장할 맥주 정보 구성하기
      beer = {}
      beer["name"] = name
      beer["abv"] = abv
      beer["country"] = country
      beer["manufacturer"] = manufacturer
      beer["beertype"] = beertype
      # 저장하기
      db.beers.insert_one(beer)
      return jsonify({"status": 200, "msg": "맥주 정보 저장하기 성공"})
   except Exception as e:
      return jsonify({"status": 500, "msg": str(e)})


@app.route("/api/user/register")
def user_register():
   try:
      # 데이터 확인하기
      formdata = request.get_json()
      formdata = request.form # temp
      username = formdata.get("username")
      password = formdata.get("password")
      if not username:
         raise Exception("유저 이름이 없습니다.")
      if not password:
         raise Exception("유저 비밀번호가 없습니다.")
      print("1111", username, password)
      hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      print("2222", username, hashed_password)
      hashed_password = hashed_password.decode('utf-8')
      print("3333", username, hashed_password)

      return jsonify({"status": 200, "msg": "사용자 등록하기 성공"})
   except Exception as e:
      return jsonify({"status": 500, "msg": str(e)})



if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)