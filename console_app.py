# console_app.py
from store import build_store
from hangman import play_hangman_game

print("hello weclcome to  musics Degree!.")

user_points = 0
store = build_store()

def play_again():
    while True:
        ans = input("\nPlay again? (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Please type 'y' or 'n'.")

def main():
    global user_points
    print("welcome to the music store goodluck connecting all the albums we have")

    while True:
        print("\n" + "=" * 50)
        print("would you like to earn points or spend points")
        print(f"score balance: {user_points}\n1.earn points\n2.spend points\n3.view owned albums\n4.exit")
        ans = input("Enter your choice (1-4): ")

        if ans == "4":
            print("thanks for playing bye bye ")
            break

        elif ans == "3":
            owned = store.get_owned_albums()
            if not owned:
                print("You don't own any albums yet!")
            else:
                print(f"\n🎵 Your Album Collection ({len(owned)} albums):")
                for album in owned:
                    band = store.get_band_by_id(album.band_id)
                    band_name = band.name if band else "Unknown"
                    print(f"  - {album.name} by {band_name}")

        elif ans == "2":
            store.display_bands()
            chosen_band = input("\nenter the band id: ").strip()

            if not chosen_band.isdigit():
                print("invalid id – must be a number")
                continue

            band_id = int(chosen_band)
            band = store.get_band_by_id(band_id)
            if band is None:
                print("band not found")
                continue

            albums_for_band = [a for a in store.get_albums_by_band(band_id) if a.availible]
            if not albums_for_band:
                print("no available albums for this band")
                continue

            print(f"\nAlbums for band id {band_id}:")
            for a in albums_for_band:
                print(f"- album id: {a.id} | name: {a.name} | price: {a.price} pts")

            chosen_album = input("\nenter the id of the album you want to buy: ").strip()
            if not chosen_album.isdigit():
                print("invalid id – must be a number")
                continue

            album_id = int(chosen_album)
            user_points = store.buy_album(album_id, user_points)

        elif ans == "1":
            while True:
                won = play_hangman_game()
                if won:
                    user_points += 10
                    print(f"You earned 10 points! New balance: {user_points}")
                if not play_again():
                    break

if __name__ == "__main__":
    main()
