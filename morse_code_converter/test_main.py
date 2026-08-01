import unittest
# Import the functions you want to test from main.py
from main import text_to_morse, morse_to_text


class TestMorseConverter(unittest.TestCase):

    # --- TESTS FOR ENCRYPTION (Text -> Morse) ---
    def test_text_to_morse_simple_word(self):
        """Test translating a simple word like 'SOS'"""
        result = text_to_morse("SOS")
        self.assertEqual(result, "... --- ...")

    def test_text_to_morse_multiple_words(self):
        """Test translating multiple words with spaces"""
        result = text_to_morse("HELLO WORLD")
        self.assertEqual(result, ".... . .-.. .-.. --- / .-- --- .-. .-.. -..")

    # --- TESTS FOR DECRYPTION (Morse -> Text) ---
    def test_morse_to_text_simple_word(self):
        """Test decrypting Morse back to text"""
        result = morse_to_text("... --- ...")
        self.assertEqual(result, "SOS")

    def test_morse_to_text_multiple_words(self):
        """Test decrypting words with '/' space separators"""
        result = morse_to_text(".... . .-.. .-.. --- / .-- --- .-. .-.. -..")
        self.assertEqual(result, "HELLO WORLD")

    def test_morse_to_text_three_spaces(self):
        """Test decrypting words with 3 spaces separators"""
        result = morse_to_text(".... . .-.. .-.. ---   .-- --- .-. .-.. -..")
        self.assertEqual(result, "HELLO WORLD")


if __name__ == "__main__":
    unittest.main()