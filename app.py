from flask import Flask, render_template, jsonify, request, session, redirect, url_for
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbAG

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/register/')
def register():
   return render_template('register.html')


if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)