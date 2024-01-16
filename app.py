from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Qwert123@localhost/game1.db'
db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(45), nullable=True)
    first_name = db.Column(db.String(45), nullable=True)
    last_name = db.Column(db.String(45), nullable=True)
    gender = db.Column(db.String(1), nullable=True)
   # birthday = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.user_id


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

@app.route('/users')
def users():
    user = User.query.order_by(User.nickname).all()
    return render_template("users.html", user=user)


@app.route('/users/<int:user_id>')
def users_detail(user_id):
    user_det = User.query.get(user_id)
    return render_template("user_detail.html", user_det=user_det)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/Add_user', methods=['POST', 'GET'])
def Add_user():
    if request.method == "POST":
        #user_id = request.form['user_id']
        nickname = request.form['nickname']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        gender = request.form['gender']
        #birthday = request.form['birthday']
        #birthday = date(2023, 3, 1)
        user = User(nickname=nickname, first_name=first_name, last_name=last_name, gender=gender) #birthday=birthday)]


        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/users')
        except:
            return "Add User was ERROR"
    else:
        return render_template("Add_user.html")


if __name__ == "__main__":
    app.run(debug=True)