from flask import jsonify, request
from . import routes

import datetime
from app import db, SECRET_KEY


@routes.route("/api/beer/get", methods=["GET"])
def get_beer():
    # params에서 맥주 아이디 체크
    # 로그인이 되어 있는 경우, 평가 정보 join
    # 다른 사람들의 평가 시간 순 정렬
    beer = {}
    return jsonify({"status": 200, "msg": "맥주 정보 불러오기 성공", "beer": beer})


@routes.route("/api/beer/list")
def get_beer_list():
    # 로그인되어 있는 경우, 각 맥주들에 대한 평가 정보 join
    beers = db.beers.find({}).sort([("created_at", -1)])
    return jsonify({"status": 200, "msg": "맥주 리스트 불러오기 성공", "beers": beers})


@routes.route("/api/beer/add", methods=["POST"])
def add_beer():
    try:
        # 데이터 확인하기
        formdata = request.get_json()
        formdata = request.form  # temp
        name = formdata.get("name")
        abv = formdata.get("abv")
        country = formdata.get("country")
        manufacturer = formdata.get("manufacturer")
        beertype = formdata.get("beertype")
        image = formdata.get("image")
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
        beer["image"] = image
        # 저장하기
        db.beers.insert_one(beer)
        return jsonify({"status": 200, "msg": "맥주 정보 저장하기 성공"})
    except Exception as e:
        return jsonify({"status": 500, "msg": str(e)})
