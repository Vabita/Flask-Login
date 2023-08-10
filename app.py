from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:VAB25102002@localhost/loginapp'
db = SQLAlchemy(app)
print(app.config['SQLALCHEMY_DATABASE_URI'])


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)



@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = Users.query.filter_by(username=username).first()

    if user:
        session['user_id'] = user.id
        return redirect(url_for('dashboard'))
    else:
        return render_template('login.html', error='Invalid username or password')


@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    if user_id:
        user = Users.query.get(user_id)
        return render_template('dashboard.html', user=user)
    else:
        return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        existing_user = Users.query.filter_by(username=username).first()
        if existing_user:
            return render_template('register.html', error='Username already exists')

        new_user = Users(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('register.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
