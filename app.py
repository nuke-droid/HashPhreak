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


class HashDB(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SHA1 = db.Column(db.String(200), nullable=False)
    SHA224 = db.Column(db.String(200), nullable=False)
    SHA256 = db.Column(db.String(200), nullable=False)
    SHA384 = db.Column(db.String(200), nullable=False)
    SHA512 = db.Column(db.String(200), nullable=False)
    __bind_key__ = 'hashes'


class query_hist(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Query %r>' % self.id



#custom hash class
class hash:
    
    #function which takes in plaintext value as strin str
    def hashgen(self, str, hashtype):
        hashtype = int(hashtype)    
        if hashtype == 1:
            result = hashlib.sha1(str.encode())
        elif hashtype == 2:
            result = hashlib.sha224(str.encode())
        elif hashtype == 3:
            result = hashlib.sha256(str.encode())
        elif hashtype == 4:
            result = hashlib.sha384(str.encode())
        elif hashtype == 5:
            result = hashlib.sha512(str.encode())
            
            
        if result != None:
            hashvalue = result.hexdigest()

        return hashvalue
    

class crackhash:
#Start time is recorded and stored for duration calulation
   def main(self):
       

        #List of exceptions is created
        e = (IndexError)

        #hash object is created as h
        h = hash()

       

        #import text file with list of commond passwords
        with open('pwd.txt') as f:
            content = f.readlines()

        #instantiates empty 2 dimensional list
        painbow = [[], []]

        #loops through text file to separate inputs
        for i in content:
            #splits each items by newline
            j = i.splitlines()
            
            #loop stores split items into plaintext and hash into two-dimensional list respectively
            for k in j:



                l = h.hashgen(k, detectedHash)

                painbow.append([k, l])
        #counter serves to provide message in the case that there is no corresponding plaintext value found for the input hash
        ticker = 0

        for i in range(len(painbow)):
            try:
                sub = painbow[i]
                #ystem('clear')

                
                #if value is found in hashses stored in memory, corresponding plaintext value is displayed and program exit
                if sub[1] == str:
                    print(f"Cracked! Password: {sub[0]} Hash: {sub[1]}")
                    ticker += 1
                
                    exit()
            
            except e:
                pass

        if ticker <= 0:
            print("No corresponding hash found in database.")
     


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
        queries = query_hist.query.order_by(query_hist.date_created).all()
        return render_template('index.html', queries=queries)


if __name__ == "__main__":
    app.run(debug=True)
