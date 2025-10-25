from flask import Flask, render_template, flash, redirect, url_for, abort, session, request, get_flashed_messages
from flask_login import LoginManager, login_required, current_user
from models import db, User, bcrypt
from auth import auth  
import os
from store import build_store
from hangman import (
    load_words,
    random_word,
    show_hidden_word,
    is_guess_valid,
    HANGMAN_PHOTOS,
    hint,
)


app = Flask(__name__)

load_words("musicians_clues.txt")

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "fallback_key")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

app.register_blueprint(auth)
bcrypt.init_app(app)

store_instance = build_store()  

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

@app.route("/hangman", methods=["GET", "POST"])
@login_required
def hangman():
    session.setdefault("guesses", [])
    session.setdefault("misses", 0)
    session["max_tries"] = 6
    session.setdefault("status", "playing")
    session.setdefault("awarded", False)
    if "word" not in session:
        session["word"] = random_word().lower().strip()

    if request.method == "POST" and session["status"] == "playing":
        guess = request.form.get("guess", "").strip().lower()

        if session['misses'] > 3 :
                clue = hint(session['word'], session['misses'])
                if clue:
                    flash(f"Hint: {clue.strip()}")
             
    
        if not guess:
                flash("Please enter a guess before submitting.")
                return redirect(url_for('hangman'))

        if not is_guess_valid(guess):
                flash("Invalid guess. Please enter a single alphabetical character that you haven't guessed before.")
                return redirect(url_for('hangman'))
        if guess in session["guesses"]:
                flash(f"You already guessed '{guess}'. Try a different letter.")
                return redirect(url_for('hangman'))
        
        if guess in session["word"]:
                flash(f"Good guess! '{guess}' is in the word.")
                session["guesses"].append(guess)
                if all(ch == " " or ch in session["guesses"] for ch in session["word"]):
                    session["status"] = "won"
                    if not session["awarded"]:
                        current_user.points += 10
                        db.session.commit()
                        session["awarded"] = True
                   
        else:
                flash(f"Sorry, '{guess}' is not in the word.")
                session["misses"] += 1
                session["guesses"].append(guess)
                if session["misses"] >= session["max_tries"]:
                    session["status"] = "lost"
                    flash(f"You've run out of tries. The word was '{session['word']}'. Better luck next time!")
    word_display = show_hidden_word(session["word"], session["guesses"]) 
    stage_key = min(session["misses"] + 1, max(HANGMAN_PHOTOS.keys()))
    hangman_art = HANGMAN_PHOTOS.get(stage_key, "")

    flash_messages = get_flashed_messages(with_categories=True)

    return render_template(
        "hangman.html",
        hangman_art=hangman_art,
        word_display=word_display,
        max_tries=session["max_tries"],
        misses=session["misses"],
        status=session["status"],
        flash_messages=flash_messages,
    )        

@app.route("/reset_hangman")
@login_required
def reset_hangman():
    session.pop("word", None)
    session.pop("guesses", None)
    session.pop("misses", None)
    session.pop("status", None)
    session.pop("awarded", None)
    return redirect(url_for('hangman'))

@app.route("/store")
@login_required
def store():
    bands = store_instance.get_bands() 
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
        flash('Album is not available.')
        return redirect(url_for('store'))

    if not store_instance.validate_purchase(album.price, current_user.points):
        flash('Not enough points to purchase this album.')
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
    app.run(host="0.0.0.0", debug=True, port=5000)
