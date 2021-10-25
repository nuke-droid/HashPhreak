from flask import Flask, redirect, url_for, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///HashPhreak.db'
db = SQLAlchemy(app)


class hist(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)


    def __repr__(self):
        return '<Entry %r>' % self.id


@app.route("/", methods=['POST', 'GET'])
def home():

    if request.method == 'POST':
        return 'hello'

    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)