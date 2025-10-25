
class MusicDegree:
    def __init__(self, item_id, name):
        self.id = item_id
        self.name = name

class Bands(MusicDegree):
    def __init__(self, item_id, name, number_of_albums, genre, availible=True):
        super().__init__(item_id, name)
        self.number = number_of_albums
        self.genre = genre
        self.availible = availible

class Albums(MusicDegree):
    def __init__(self, item_id, name, price, availible=True, band_id=None):
        super().__init__(item_id, name)
        self.price = price
        self.band_id = band_id
        self.availible = availible


class musicstore():
    def __init__(self):
        self.items = []

    
    def get_albums(self):
        return [item for item in self.items if isinstance(item, Albums)]

    def get_bands(self):
        return [item for item in self.items if isinstance(item, Bands)]

    def get_band_by_id(self, band_id: int):
        return next((b for b in self.get_bands() if b.id == band_id), None)

    def get_album_by_id(self, album_id: int):
        return next((a for a in self.get_albums() if a.id == album_id), None)

    def add_item(self, item):
        self.items.append(item)

   
    def display_bands(self):
        bands = self.get_bands()
        availible_bands = [band for band in bands if band.availible]
        for band in availible_bands:
            print(f"id: {band.id}  '{band.name}'  albums: {band.number} ({band.genre})")

    def buy_album(self, album_id, user_points):
        album = self.get_album_by_id(album_id)
        if album is None:
            print("Album not found")
            return user_points
        if not album.availible:
            print("This album is already owned")
            return user_points
        if album.price > user_points:
            print(f"Not enough points! You need {album.price} but only have {user_points}")
            return user_points
        
        album.availible = False
        user_points -= album.price
        print(f"✓ '{album.name}' is now yours! Remaining balance: {user_points}")
        return user_points

    def display_albums(self):
        albums = self.get_albums()
        availible_album = [album for album in albums if album.availible]
        for album in availible_album:
            print(f"id: {album.id} name: {album.name} price: {album.price} pts")

    def get_owned_albums(self):
        return [album for album in self.get_albums() if not album.availible]

    def get_albums_by_band(self, band_id: int):
        return [a for a in self.get_albums() if getattr(a, "band_id", None) == band_id]

    def validate_purchase(self, price, user_points):
        return user_points >= price


def build_store():
    
    store = musicstore()

    
    band1 = Bands(1, "The Beatles", 5, "rock")
    band2 = Bands(2, "The Rolling Stones", 3, "rock")
    band3 = Bands(3, "Led Zeppelin", 8, "hard rock")
    band4 = Bands(4, "Pink Floyd", 6, "progressive rock")
    band5 = Bands(5, "Queen", 7, "rock")
    band6 = Bands(6, "Black Sabbath", 3, "heavy metal")
    band7 = Bands(7, "Metallica", 6, "heavy metal")
    band8 = Bands(8, "Nirvana", 4, "grunge")
    band9 = Bands(9, "guns&roses", 5, "rock")

    bands_list = [band1, band2, band3, band4, band5, band6, band7, band8, band9]
    for item in bands_list:
        store.add_item(item)

   
    # The Beatles (band_id = 1)
    album1 = Albums(1, "Please Please Me", 10, band_id=1)
    album2 = Albums(2, "Revolver", 15, band_id=1)
    album3 = Albums(3, "Sgt. Pepper's Lonely Hearts Club Band", 20, band_id=1)
    album4 = Albums(4, "Abbey Road", 20, band_id=1)

    # The Rolling Stones (band_id = 2)
    album5 = Albums(5, "Let It Bleed", 12, band_id=2)
    album6 = Albums(6, "Sticky Fingers", 15, band_id=2)
    album7 = Albums(7, "Exile on Main St.", 18, band_id=2)

    # Led Zeppelin (band_id = 3)
    album8 = Albums(8, "Led Zeppelin I", 14, band_id=3)
    album9 = Albums(9, "Led Zeppelin II", 16, band_id=3)
    album10 = Albums(10, "Led Zeppelin IV", 20, band_id=3)
    album11 = Albums(11, "Physical Graffiti", 22, band_id=3)

    # Pink Floyd (band_id = 4)
    album12 = Albums(12, "The Dark Side of the Moon", 25, band_id=4)
    album13 = Albums(13, "Wish You Were Here", 20, band_id=4)
    album14 = Albums(14, "Animals", 18, band_id=4)
    album15 = Albums(15, "The Wall", 25, band_id=4)

    # Queen (band_id = 5)
    album16 = Albums(16, "Sheer Heart Attack", 16, band_id=5)
    album17 = Albums(17, "A Night at the Opera", 20, band_id=5)
    album18 = Albums(18, "News of the World", 18, band_id=5)

    # Black Sabbath (band_id = 6)
    album19 = Albums(19, "Black Sabbath", 14, band_id=6)
    album20 = Albums(20, "Paranoid", 16, band_id=6)
    album21 = Albums(21, "Master of Reality", 15, band_id=6)

    # Metallica (band_id = 7)
    album22 = Albums(22, "Kill 'Em All", 15, band_id=7)
    album23 = Albums(23, "Ride the Lightning", 18, band_id=7)
    album24 = Albums(24, "Master of Puppets", 20, band_id=7)
    album25 = Albums(25, "Metallica (The Black Album)", 22, band_id=7)

    # Nirvana (band_id = 8)
    album26 = Albums(26, "Bleach", 12, band_id=8)
    album27 = Albums(27, "Nevermind", 20, band_id=8)
    album28 = Albums(28, "In Utero", 18, band_id=8)

    # Guns N' Roses (band_id = 9)
    album29 = Albums(29, "Appetite for Destruction", 20, band_id=9)
    album30 = Albums(30, "G N' R Lies", 14, band_id=9)
    album31 = Albums(31, "Use Your Illusion I", 18, band_id=9)
    album32 = Albums(32, "Use Your Illusion II", 18, band_id=9)

    albums_list = [
        album1, album2, album3, album4,      # The Beatles
        album5, album6, album7,              # The Rolling Stones
        album8, album9, album10, album11,    # Led Zeppelin
        album12, album13, album14, album15,  # Pink Floyd
        album16, album17, album18,           # Queen
        album19, album20, album21,           # Black Sabbath
        album22, album23, album24, album25,  # Metallica
        album26, album27, album28,           # Nirvana
        album29, album30, album31, album32   # Guns N' Roses
    ]
    for item in albums_list:
        store.add_item(item)

    return store
