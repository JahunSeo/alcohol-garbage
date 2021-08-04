from flask import jsonify, request
from . import routes
from bson.objectid import ObjectId
import datetime
from app import db


@routes.route("/api/review/add", methods=["POST"])
def add_review():
    try:
        # 데이터 확인하기
        formdata = request.form
        username = formdata.get("username")
        beer_id = formdata.get("beer_id")
        score = formdata.get("score")
        comment = formdata.get("comment")
        if not username:
            raise Exception("사용자 이름이 없습니다.")
        if not beer_id:
            raise Exception("맥주 아이디가 없습니다.")
        if not score:
            raise Exception("점수가 없습니다.")
        if not comment:
            raise Exception("한줄평이 없습니다.")  
        # 저장할 리뷰 구성하기
        review = {}
        review["username"] = username
        review["beer_id"] = ObjectId(beer_id)
        review["score"] = int(score)
        review["comment"] = comment
        review["created_at"] = datetime.datetime.utcnow()
        review["updated_at"] = datetime.datetime.utcnow()
        # 저장하기
        db.reviews.insert_one(review)
        return jsonify({"status": 200, "msg": "리뷰 저장하기 성공"})
    except Exception as e:
        return jsonify({"status": 500, "msg": str(e)})


@routes.route("/api/review/update", methods=["POST"])
def update_review():
    try:
        formdata = request.form
        _id = formdata.get("_id")
        score = formdata.get("score")
        comment = formdata.get("comment")
        if not _id:
            raise Exception("리뷰 아이디가 없습니다.")
        if not score:
            raise Exception("점수가 없습니다.")
        if not comment:
            raise Exception("한줄평이 없습니다.")  
        # 수정할 리뷰 구성하기
        review = {}
        review["score"] = score
        review["comment"] = comment
        review["updated_at"] = datetime.datetime.utcnow()
        # 수정하기
        db.reviews.update_one({"_id": ObjectId(_id)}, {"$set": review})
        return jsonify({"status": 200, "msg": "리뷰 수정하기 성공"})
    except Exception as e:
        return jsonify({"status": 500, "msg": str(e)})


@routes.route("/api/review/delete", methods=["POST"])
def delete_review():
    try:
        # 데이터 확인하기
        formdata = request.form
        _id = formdata.get("_id")
        if not _id:
            raise Exception("삭제할 리뷰의 아이디가 없습니다.")
        # 삭제하기
        db.reviews.delete_one({"_id": ObjectId(_id)})
        return jsonify({"status": 200, "msg": "리뷰 삭제하기 성공"})
    except Exception as e:
        return jsonify({"status": 500, "msg": str(e)})