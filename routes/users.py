from flask import jsonify, request
from . import routes

from flask_jwt_extended import *
import bcrypt

from app import db

@routes.route("/api/user/login", methods=["POST"])
def user_login():
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
      # 유저 찾기
      user = db.users.find_one({"username": username})
      if user is None:
         raise Exception("잘못된 유저 이름입니다.")
      # 비밀번호 체크하기
      check_pw = bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8'))
      print(username, password, check_pw)
      if not check_pw:
         raise Exception("잘못된 비밀번호입니다.")
      # token 생성하기
      access_token = create_access_token(identity=username, expires_delta=False)
      refresh_token = create_refresh_token(identity=username)
      
      resp = jsonify({"status": 200, "msg": "사용자 로그인 성공"})
      set_access_cookies(resp, access_token)
      set_refresh_cookies(resp, refresh_token)
      return resp
   except Exception as e:
      return jsonify({"status": 500, "msg": str(e)})



@routes.route("/api/user/register", methods=["POST"])
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
      # 비밀번호 암호화하기
      hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
      hashed_password = hashed_password.decode('utf-8')
      # 이미 동일한 username이 있는지 확인
      prev = db.users.find_one({"username": username})
      if prev:
         raise Exception("이미 동일한 이름의 유저가 있습니다.")
      # 저장할 정보 구성하기
      user = {}
      user["username"] = username
      user["password"] = hashed_password
      # 저장하기
      db.users.insert_one(user)
      return jsonify({"status": 200, "msg": "사용자 등록하기 성공"})
   except Exception as e:
      return jsonify({"status": 500, "msg": str(e)})

# @routes.route("/api/user/check", methods=["GET"])
# def user_check():
#     try:
#         token = request.headers["token"]
#         payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#         user = db.users.find_one({"username": payload["username"]})
#         if user is None:
#             raise Exception("토큰으로 정보를 확인할 수 없습니다.")
#         return jsonify({"status": 200, "msg": "사용자 체크 성공", "username": user["username"]})
#     except jwt.ExpiredSignatureError:
#         return jsonify({"status": 500, "msg": "로그인 시간 만료"})
#     except Exception as e:
#       return jsonify({"status": 500, "msg": str(e)})
