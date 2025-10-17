import unittest

from store import build_store, Albums


class StoreTestCase(unittest.TestCase):
    def setUp(self):
        self.store = build_store()

    def test_band_catalogue_count(self):
        bands = self.store.get_bands()
        self.assertEqual(len(bands), 9)

    def test_album_catalogue_count(self):
        albums = self.store.get_albums()
        self.assertTrue(len(albums) >= 30)

    def test_get_album_by_id(self):
        album = self.store.get_album_by_id(1)
        self.assertIsInstance(album, Albums)
        self.assertEqual(album.id, 1)

    def test_get_owned_albums(self):
        album = self.store.get_album_by_id(1)
        album.availible = False
        owned = self.store.get_owned_albums()
        self.assertIn(album, owned)

    def test_validate_purchase(self):
        album = self.store.get_album_by_id(1)
        self.assertTrue(self.store.validate_purchase(album.price, album.price))
        self.assertFalse(self.store.validate_purchase(album.price, album.price - 1))


if __name__ == "__main__":
    unittest.main()
