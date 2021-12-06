from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query
from datetime import datetime
import hashlib
import time
from os import strerror, system

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HashPhreak.db'
app.config['SQLALCHEMY_BINDS'] = {'hashes' : 'sqlite:///hashes.db'}
db = SQLAlchemy(app)


class query_hist(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


class HashDB(db.Model):
    _bind_key__ = 'hashes'
    id = db.Column(db.Integer, primary_key=True)
    S1 = db.Column(db.String(200), nullable=False)
    S224 = db.Column(db.String(200), nullable=False)
    S256 = db.Column(db.String(200), nullable=False)
    S384 = db.Column(db.String(200), nullable=False)
    S512 = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

   
    def HASH_DIGEST():
        
        with open('rockyou.txt') as f:
            content = f.readlines()
        
        for i in content:

            j = i.splitlines()

            for k in j:

                result1 = hashlib.sha1(str.encode())
                result224 = hashlib.sha224(str.encode())
                result256 = hashlib.sha256(str.encode())
                result384 = hashlib.sha384(str.encode())
                result512 = hashlib.sha512(str.encode())

               

                new_hash =  HashDB(S1 = result1, S224 = result224, S256 = result256, S384 = result384, S512 = result512)

                db.session.add(new_hash)
                db.session.commit()
 
  
@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        query_content = request.form['content']
        new_query = query_hist(content=query_content)
        try:
            db.session.add(new_query)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with your query'

    else:
        queries = HashDB.query.order_by(HashDB.date_created).all()
        return render_template('index.html', queries=queries)


if __name__ == "__main__":
    app.run(debug=True)
