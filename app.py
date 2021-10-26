from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import query
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HashPhreak.db'
db = SQLAlchemy(app)


class query_hist(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Query %r>' % self.id


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
