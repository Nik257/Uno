from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
db = SQLAlchemy(app)

# таблица Юзеры
class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    nickname = db.Column(db.String(45), nullable=True)
    first_name = db.Column(db.String(45), nullable=True)
    last_name = db.Column(db.String(45), nullable=True)
    gender = db.Column(db.String(1), nullable=True)
    birthday = db.Column(db.Date, nullable=False)
    results = db.relationship('Result', backref='user', lazy=True)


    def __repr__(self):
        return '<User %r>' % self.user_id

# таблица игр которые будут добавляться
class Kon(db.Model):
    kon_id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    round = db.Column(db.Integer, nullable=True)
    comment = db.Column(db.String(250), nullable=False)
    results = db.relationship('Result', backref='kon', lazy=True)

    def __repr__(self):
        return '<Kon %r>' % self.kon_id

# таблица результатов по играм
class Result(db.Model):
    result_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    kon_id = db.Column(db.Integer, db.ForeignKey('kon.kon_id'), nullable=False)
    resultat = db.Column(db.Integer,  nullable=True)
    is_winner = db.Column(db.Boolean, nullable=True)
    price = db.Column(db.Integer, nullable=True)

    #fk_user = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    #user = db.relationship('User', backref=db.backref('kons', lazy=True))

    #fk_kon = db.Column(db.Integer, db.ForeignKey('kon.kon_id'), nullable=False)
    #kon = db.relationship('Kon', backref=db.backref('results', lazy=True))

    def __repr__(self):
        return '<Result %r>' % self.result_id

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")

# страница юзера
@app.route('/users')
def users():
    user = User.query.order_by(User.nickname).all()
    return render_template("users.html", user=user)

# Добавление пользователей на страницу пользователей через кнопку добавления
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

@app.route('/kons')
def kons():
    kon = Kon.query.order_by(Kon.kon_id).all()
    return render_template("kons.html", kon=kon)

# Добавление игры в базу kon, через кпопку добавить
@app.route('/add_kon', methods=['POST', 'GET'])
def add_kon():
    if request.method == "POST":
        #kon_id = request.form['kon_id']
        date = datetime.strptime(request.form['date'], "%Y-%m-%d")
        round = request.form['round']
        comment = request.form['comment']
        kon = Kon(date=date, round=round, comment=comment)


        try:
            db.session.add(kon)
            db.session.commit()
            return redirect('/kons')
        except:
            return "Add Kon was ERROR"
    else:
        return render_template("add_kon.html")

# детали по игре
@app.route('/kons/<int:kon_id>')
def kon_detail(kon_id):
    kon_det = Kon.query.get(kon_id)
    return render_template("kon_detail.html", kon_det=kon_det)


# удаление игры из таблицы
@app.route('/kons/<int:kon_id>/delete')
def kon_delete(kon_id):
    kon_det = Kon.query.get_or_404(kon_id)

    try:
        db.session.delete(kon_det)
        db.session.commit()
        return redirect('/kons')
    except:
        return "Delete kon was mistake"


# редактирование игры из таблицы
@app.route('/kons/<int:kon_id>/update', methods=['POST', 'GET'])
def kon_update(kon_id):
    kon_det = Kon.query.get(kon_id)
    if request.method == "POST":
        #kon_det.kon_id = request.form['kon_id']
        kon_det.date = datetime.strptime(request.form['date'], "%Y-%m-%d")
        kon_det.round = request.form['round']
        kon_det.comment = request.form['comment']

        try:
            db.session.commit()
            return redirect('/kons')
        except:
            return "Add Kon was ERROR"
    else:
        return render_template("kon_update.html", kon_det=kon_det)


#страница результата
@app.route('/results')
def results():
    result = Result.query.order_by(Result.result_id).all()
    return render_template("results.html", result=result)


# Добавление результата по игре через кнопку добавления
@app.route('/add_result', methods=['POST', 'GET'])
def add_result():
    if request.method == "POST":
        user_id = int(request.form['user_id'])
        kon_id = int(request.form['kon_id'])
        resultat = request.form['resultat']
        is_winner = bool(request.form['is_winner'])
        price = int(request.form['price'])
        result = Result(user_id=user_id, kon_id=kon_id, resultat=resultat, is_winner=is_winner, price=price)

        try:
            db.session.add(result)
            db.session.commit()
            return redirect('/results')
        except Exception as error:
            print(error)
            return "Add result was ERROR"
    else:
        return render_template("add_result.html")

# детали по результате
@app.route('/results/<int:result_id>')
def result_detail(result_id):
    result_det = Result.query.get(result_id)
    return render_template("result_detail.html", result_det=result_det)



# удаление результата из таблицы
@app.route('/results/<int:result_id>/delete')
def result_delete(result_id):
    result_det = Result.query.get_or_404(result_id)

    try:
        db.session.delete(result_det)
        db.session.commit()
        return redirect('/results')
    except:
        return "Delete result was mistake"
@app.route('/about')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)