from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

db = SQLAlchemy()
bcrypt = Bcrypt()

# Association table for many-to-many relationship between users and albums
user_albums = db.Table('user_albums',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    points = db.Column(db.Integer, default=100)
    albums = db.relationship('Album', secondary=user_albums, backref='owners')

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self):
        return f"User('{self.username}')"

class Band(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(50))
    albums = db.relationship('Album', backref='band', lazy=True)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    band_id = db.Column(db.Integer, db.ForeignKey('band.id'), nullable=False)