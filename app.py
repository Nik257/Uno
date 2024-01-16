from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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
    birthday = db.Column(db.Date, nullable=False)


    def __repr__(self):
        return '<User %r>' % self.user_id


class Kon(db.Model):
    kon_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    round = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(250), nullable=False)

    def __repr__(self):
        return '<Kon %r>' % self.kon_id


class Result(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    kon_id = db.Column(db.Integer, primary_key=True)
    result = db.Column(db.Integer,  nullable=True)
    is_winner = db.Column(db.Boolean, nullable=True)
    price = db.Column(db.Integer, nullable=True)

    fk_user = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('kons', lazy=True))

    fk_kon = db.Column(db.Integer, db.ForeignKey('kon.kon_id'), nullable=False)
    kon = db.relationship('Kon', backref=db.backref('results', lazy=True))

    def __repr__(self):
        return '<Result %r>' % self.user_id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/users')
def users():
    user = User.query.order_by(User.nickname).all()
    return render_template("users.html", user=user)


@app.route('/kons')
def kons():
    kon = Kon.query.order_by(Kon.kon_id).all()
    return render_template("kons.html", kon=kon)


@app.route('/results')
def results():
    result = Result.query.order_by(Result.user_id).all()
    return render_template("results.html", result=result)

# детали по пользователю
@app.route('/users/<int:user_id>')
def users_detail(user_id):
    user_det = User.query.get(user_id)
    return render_template("user_detail.html", user_det=user_det)


# удаление пользователя из таблицы
@app.route('/users/<int:user_id>/delete')
def users_delete(user_id):
    user_det = User.query.get_or_404(user_id)

    try:
        db.session.delete(user_det)
        db.session.commit()
        return redirect('/users')
    except:
        return "Delete user was mistake"


# редактирование пользователя из таблицы
@app.route('/users/<int:user_id>/update', methods=['POST', 'GET'])
def user_update(user_id):
    user_det = User.query.get(user_id)
    if request.method == "POST":
        user_det.nickname = request.form['nickname']
        user_det.first_name = request.form['first_name']
        user_det.last_name = request.form['last_name']
        user_det.gender = request.form['gender']
        user_det.birthday = datetime.strptime(request.form['birthday'], "%Y-%m-%d")


        try:
            db.session.commit()
            return redirect('/users')
        except:
            return "Add User was ERROR"
    else:
        return render_template("user_update.html", user_det=user_det)

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
        birthday = datetime.strptime(request.form['birthday'], "%Y-%m-%d")
        user = User(nickname=nickname, first_name=first_name, last_name=last_name, gender=gender, birthday=birthday)


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