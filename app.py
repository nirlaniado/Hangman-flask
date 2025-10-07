from flask import Flask, render_template
from flask_login import LoginManager
from models import db, User, bcrypt
from auth import auth  

app = Flask(__name__)

app.config['SECRET_KEY'] = 'something_secret_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///music_shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

app.register_blueprint(auth)
bcrypt.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def welcome():
    return render_template("index.html")

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Database initialized!')

if __name__ == "__main__":
    app.run(debug=True, port=5000)