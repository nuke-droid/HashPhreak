from operator import contains, or_
from pickle import NONE
import re
from string import hexdigits
from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from requests import Session
from sqlalchemy.orm import query
from datetime import datetime
import hashlib
import time
from os import strerror, system

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HashPhreak.db'
app.config['SQLALCHEMY_BINDS'] = {'hashes' : 'sqlite:///hashes.db'}
db = SQLAlchemy(app)







class HASH_DB(db.Model):
    __bind_key__ = 'hashes'
    id = db.Column(db.Integer, primary_key=True)
    PLAINTEXT = db.Column(db.String(200), nullable=False)
    S1 = db.Column(db.String(200), nullable=False)
    S224 = db.Column(db.String(200), nullable=False)
    S256 = db.Column(db.String(200), nullable=False)
    S384 = db.Column(db.String(200), nullable=False)
    S512 = db.Column(db.String(200), nullable=False)

    #date_created = db.Column(db.DateTime, default=datetime.utcnow)
    word_list = '.\rockyou.txt'
    word_list_hash = 'temp'

    def HASH_DIGEST():
        #global word_list
        with open('rockyou.txt', encoding="utf8") as f:
            content = f.readlines()
        
        for i in content:

            j = i.splitlines()

            for str in j:

                result1 = (hashlib.sha1(str.encode())).hexdigest()
                result224 = (hashlib.sha224(str.encode())).hexdigest()
                result256 = (hashlib.sha256(str.encode())).hexdigest()
                result384 = (hashlib.sha384(str.encode())).hexdigest()
                result512 = (hashlib.sha512(str.encode())).hexdigest()

               

                new_hash =  HASH_DB(PLAINTEXT = str, S1 = result1, S224 = result224, S256 = result256, S384 = result384, S512 = result512)

                db.session.add(new_hash)
                db.session.commit()

    def HASH_FILE():
    #This function returns the SHA-1 hash of the file passed into it
        #make hash object
        h = hashlib.sha1()
        global word_list
        #global word_list_hash
        
        #open file in binary format
        with open('rockyou.txt', 'rb') as file:
            
            #loop until EOF
            chunk = 0
            
            
            while chunk != b'':
                chunk = file.read(1024)
                h.update(chunk)
        
        if HASH_DB.word_list_hash != h.hexdigest():
            
            HASH_DB.word_list_hash = h.hexdigest()
            HASH_DB.HASH_DIGEST()
        
        else:
            pass

class SEARCH_QUERY(db.Model):
    __bind_key__ = 'hashes'
    id= db.Column(db.Integer, primary_key=True)
    entry = db.Column(db.String(200), nullable=False)
    PLAINTEXT = db.Column(db.String(200), nullable=False)
    S1 = db.Column(db.String(200), nullable=False)
    S224 = db.Column(db.String(200), nullable=False)
    S256 = db.Column(db.String(200), nullable=False)
    S384 = db.Column(db.String(200), nullable=False)
    S512 = db.Column(db.String(200), nullable=False)
    #date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def HASH_RESULT():
        entry1 = request.form['content']
        #search_v = "{0}".format(entry1)
        results = HASH_DB.query.filter(or_(HASH_DB.PLAINTEXT.contains(entry1), 
                                            HASH_DB.S1.contains(entry1),
                                            HASH_DB.S224.contains(entry1),
                                            HASH_DB.S256.contains(entry1),
                                            HASH_DB.S384.contains(entry1),
                                            HASH_DB.S512.contains(entry1))).all()
        #results = NONE
        #results = db.session.query(HASH_DB).all()
        
        empty = []
        if (results != empty):
           
        
            #new_search =  SEARCH_QUERY(entry = entry1, PLAINTEXT = results[1], S1 = results[2], S224 = results[3], S256 = results[4], S384 = results[5], S512 = results[6])
                
            #db.session.add(new_search)
                
            #d#b.session.commit()
            
            print(results)
        
            
            

        else:
            new_search =  SEARCH_QUERY(entry = entry1, PLAINTEXT = 'NF', S1 = 'NF', S224 = 'NF', S256 = 'NF', S384 = 'NF', S512 = 'NF')

            db.session.add(new_search)
            db.session.commit()
            return results

  
@app.route("/", methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        #query_content = request.form['content']
    
        #new_query = SEARCH_QUERY(entry=query_content)
        try:
            SEARCH_QUERY.HASH_RESULT()
            #time.sleep(5)
            return redirect('/')
        except:
            return 'There was an issue with your query'
            #return query_content

    else:
        queries = SEARCH_QUERY.query.order_by(SEARCH_QUERY.id).all()
        #HASH_DB.HASH_FILE()
        return render_template('index.html', queries=queries)


if __name__ == "__main__":
    app.run(debug=True)
