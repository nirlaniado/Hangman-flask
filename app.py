from flask import Flask, render_template, flash, redirect, url_for, abort
from flask_login import LoginManager, login_required, current_user
from models import db, User, bcrypt
from auth import auth  
from store import build_store

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

store_instance = build_store()  # Create a single instance

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route("/")
def welcome():
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

@app.route("/hangman")
@login_required
def hangman():
    pass

@app.route("/store")
@login_required
def store():
    bands = store_instance.get_bands()  # Use store_instance instead of store
    return render_template("bands.html", bands=bands)

@app.route("/owned-albums")
@login_required
def owned_albums():
    owned = store_instance.get_owned_albums()
    bands_by_id = {band.id: band for band in store_instance.get_bands()}
    return render_template("owned_band.html", albums=owned, bands_by_id=bands_by_id)

@app.route('/band_albums/<int:band_id>')
@login_required
def band_albums(band_id):
    band = store_instance.get_band_by_id(band_id)
    if band is None:
        abort(404)
    albums = [album for album in store_instance.get_albums_by_band(band_id) if album.availible]
    if not albums:
        flash('You have all albums from this band!', 'info')
    return render_template('band_albums.html', band=band, albums=albums)

@app.route('/purchase_album/<int:album_id>', methods=['POST'])
@login_required
def purchase_album(album_id):
    album = store_instance.get_album_by_id(album_id)
    if album is None or not album.availible:
        flash('Album is not available.', 'error')
        return redirect(url_for('store'))

    if not store_instance.validate_purchase(album.price, current_user.points):
        flash('Not enough points to purchase this album.', 'error')
        return redirect(url_for('band_albums', band_id=album.band_id))

    current_user.points -= album.price
    album.availible = False
    db.session.commit()
    flash(f'Successfully purchased {album.name}!', 'success')

    return redirect(url_for('band_albums', band_id=album.band_id))

@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('Database initialized!')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
