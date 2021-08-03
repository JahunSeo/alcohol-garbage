from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbloginSystem2

# JWT 토큰을 만들 때 필요한 비밀문자열입니다. 아무거나 입력해도 괜찮습니다.
# 이 문자열은 서버만 알고있기 때문에, 내 서버에서만 토큰을 인코딩(=만들기)/디코딩(=풀기) 할 수 있습니다.
SECRET_KEY = 'secret'

# JWT 패키지를 사용합니다. (설치해야할 패키지 이름: PyJWT)
import jwt

# 토큰에 만료시간을 줘야하기 때문에, datetime 모듈도 사용합니다.
import datetime

# 회원가입 시엔, 비밀번호를 암호화하여 DB에 저장해두는 게 좋습니다.
# 그렇지 않으면, 개발자(=나)가 회원들의 비밀번호를 볼 수 있으니까요.^^;
import hashlib

#################################
##  HTML을 주는 부분             ##
#################################
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login')
def login():
   return render_template('login.html')

@app.route('/register')
def register():
   return render_template('register.html')

#################################
##  로그인을 위한 API            ##
#################################

@app.route('/api/register', methods=['POST'])
def api_register():
   userid_receive = request.form['userid_give']
   pw_receive = request.form['pw_give']
   nickname_receive = request.form['nickname_give']

   pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

   db.user.insert_one({'userid':userid_receive,'pw':pw_hash, 'nickname': nickname_receive })

   return jsonify({'result': 'success'})

# [로그인 API]
# id, pw를 받아서 맞춰보고, 토큰을 만들어 발급
@app.route('/api/login', methods=['POST'])
def api_login():
   userid_receive = request.form['userid_give']
   pw_receive = request.form['pw_give']
   
   pw_hash = hashlib.sha256(pw_receive.encode('utf-8')).hexdigest()

   result = db.user.find_one({'userid':userid_receive,'pw':pw_hash })

   if result is not None:
      payload = {
         'userid': userid_receive,
         'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=30) #만료시간
      }
      token = jwt.encode(payload, SECRET_KEY, algorithm='HS256') 
      #str object는 decoding된 상태이므로, decoding할 필요 없음
      # str --> bytes 로 encoding // bytes--> str로 decoding
      return jsonify({'result': 'success', 'token' : token})

   else:
      return jsonify({'result': 'fail', 'msg':'아이디 또는 비밀번호가 일치하지 않습니다.'})

# [유저 정보 확인 API]
# 로그인된 유저만 call 할 수 있는 API.
# 유효한 토큰을 줘야 올바른 결과를 얻어갈 수 있습니다.
@app.route('/api/check', methods=['GET'])
def api_check():
   token_receive = request.headers['token_give']

   try:
      payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
      userinfo = db.user.find_one({'userid':payload['userid']},{'_id': False})
      return jsonify({'result': 'success', 'nickname' : userinfo['nickname']}) 
   except jwt.ExpiredSignatureError:
      return jsonify({'result': 'fail', 'msg':'로그인 시간이 만료되었습니다.'})


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)