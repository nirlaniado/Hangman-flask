import unittest

import hangman
from hangman import show_hidden_word, is_guess_valid, hint


class HangmanLogicTestCase(unittest.TestCase):
    def setUp(self):
        hangman.word_dict.clear()
        hangman.word_dict["queen"] = "Legendary band"

    def test_show_hidden_word_masks_letters(self):
        result = show_hidden_word("queen", ["q", "e"])
        self.assertEqual(result, "q-ee-")

    def test_show_hidden_word_preserves_spaces(self):
        result = show_hidden_word("pink floyd", ["p", "o"])
        self.assertEqual(result, "p--- --o--")

    def test_is_guess_valid(self):
        self.assertTrue(is_guess_valid("a"))
        self.assertFalse(is_guess_valid("ab"))
        self.assertFalse(is_guess_valid("1"))

    def test_hint_requires_enough_misses(self):
        self.assertEqual(hint("queen", 3), "")
        self.assertEqual(hint("queen", 4), "Legendary band")


if __name__ == "__main__":
    unittest.main()
